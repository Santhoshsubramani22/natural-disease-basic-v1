import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, jsonify, g
from config import Config
from services.ml_service import ml_service
from services.ai_service import AIService
from services.alert_service import AlertService
from services.translation_service import TRANSLATIONS

app = Flask(__name__)
app.config.from_object(Config)

# Database Initialization
def init_db():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            disaster_type TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            location_name TEXT,
            probability REAL,
            risk_score INTEGER,
            risk_level TEXT,
            severity INTEGER,
            alert_level TEXT,
            model_used TEXT,
            explanation TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            disaster_type TEXT NOT NULL,
            location TEXT,
            risk_score INTEGER,
            alert_level TEXT,
            message TEXT,
            status TEXT DEFAULT 'Unread'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Page Routes
@app.route('/')
def page_index():
    return render_template('index.html')

@app.route('/dashboard')
def page_dashboard():
    return render_template('dashboard.html')

@app.route('/prediction')
def page_prediction():
    return render_template('prediction.html')

@app.route('/analytics')
def page_analytics():
    return render_template('analytics.html')

@app.route('/models')
def page_models():
    return render_template('models.html')

@app.route('/map')
def page_map():
    return render_template('map.html', google_maps_api_key=Config.GOOGLE_MAPS_API_KEY)

@app.route('/alerts')
def page_alerts():
    return render_template('alerts.html')

@app.route('/history')
def page_history():
    return render_template('history.html')

# API Endpoints
@app.route('/api/disasters', methods=['GET'])
def api_disasters():
    return jsonify({"disasters": Config.DISASTER_TYPES, "algorithms": Config.ALGORITHMS})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json() or {}
    disaster_type = data.get("disaster_type", "Flood")
    algorithm = data.get("algorithm", "random_forest")
    location_name = data.get("location_name", "Specified Location")
    lat = float(data.get("latitude", 0.0))
    lng = float(data.get("longitude", 0.0))

    # Input Validation Example
    humidity = float(data.get("humidity_percent", 50))
    if not (0 <= humidity <= 100):
        return jsonify({"error": "Humidity percentage must be between 0 and 100"}), 400

    try:
        res = ml_service.predict(data, disaster_type, algorithm)
        
        # Call AI Service for narrative explanation & alerts
        ai_res = AIService.generate_explanation(
            disaster_type=disaster_type,
            location=location_name,
            probability=res["probability"],
            risk_score=res["risk_score"],
            risk_level=res["risk_level"],
            severity=res["severity"],
            top_factors=res["top_factors"]
        )

        res["explanation"] = ai_res["explanation"]
        res["alert_message"] = ai_res["warning_message"]
        res["recommendations"] = ai_res["recommendations"]

        # Store in SQLite Prediction History
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions 
            (disaster_type, latitude, longitude, location_name, probability, risk_score, risk_level, severity, alert_level, model_used, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (disaster_type, lat, lng, location_name, res["probability"], res["risk_score"], 
              res["risk_level"], res["severity"], res["alert_level"], algorithm, res["explanation"]))
        conn.commit()
        conn.close()

        # Trigger High Risk Alert automatically
        if res["risk_score"] >= 70:
            AlertService.create_alert(
                disaster_type=disaster_type,
                location=location_name,
                risk_score=res["risk_score"],
                alert_level=res["alert_level"],
                message=res["alert_message"]
            )

        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM predictions")
    total_predictions = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM predictions WHERE risk_score >= 70")
    high_risk = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM alerts WHERE status = 'Unread'")
    active_alerts = cursor.fetchone()['total']

    cursor.execute("SELECT AVG(risk_score) as avg_score FROM predictions")
    avg_row = cursor.fetchone()
    avg_score = round(avg_row['avg_score'], 1) if avg_row['avg_score'] else 0.0

    # Risk level breakdown
    cursor.execute("SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level")
    risk_dist = {row['risk_level']: row['count'] for row in cursor.fetchall()}

    # Recent predictions
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 5")
    recent_preds = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return jsonify({
        "metrics": {
            "total_predictions": total_predictions,
            "high_risk_predictions": high_risk,
            "active_alerts": active_alerts,
            "average_risk_score": avg_score
        },
        "risk_distribution": risk_dist,
        "recent_predictions": recent_preds
    })

@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    df = pd.read_csv(Config.DATASET_PATH)
    
    # Dataset statistics calculated directly from CSV
    disaster_counts = {
        "Flood": int(df["flood_occurrence"].sum()),
        "Earthquake": int(df["earthquake_occurrence"].sum()),
        "Cyclone": int(df["cyclone_occurrence"].sum()),
        "Wildfire": int(df["wildfire_occurrence"].sum()),
        "Landslide": int(df["landslide_occurrence"].sum()),
        "Drought": int(df["drought_occurrence"].sum()),
        "Tsunami": int(df["tsunami_occurrence"].sum())
    }

    # Bivariate data samples for charts (limit sample size for responsive rendering)
    scatter_data = {
        "flood": df[["rainfall_24h_mm", "flood_occurrence"]].head(200).to_dict(orient="records"),
        "wildfire": df[["temperature_c", "wildfire_occurrence"]].head(200).to_dict(orient="records"),
        "cyclone": df[["wind_speed_kmh", "cyclone_occurrence"]].head(200).to_dict(orient="records"),
        "earthquake": df[["earthquake_magnitude", "earthquake_occurrence"]].head(200).to_dict(orient="records")
    }

    return jsonify({
        "total_records": len(df),
        "disaster_counts": disaster_counts,
        "scatter_samples": scatter_data
    })

@app.route('/api/map-data', methods=['GET'])
def api_map_data():
    df = pd.read_csv(Config.DATASET_PATH)
    disaster_filter = request.args.get("disaster", "All")
    risk_filter = request.args.get("risk", "All")

    # Sample dataset records for map markers
    sample_df = df.sample(n=min(300, len(df)), random_state=42)
    markers = []

    for _, r in sample_df.iterrows():
        # Determine disaster type for marker
        d_type = "Flood"
        if r.get("earthquake_occurrence") == 1: d_type = "Earthquake"
        elif r.get("cyclone_occurrence") == 1: d_type = "Cyclone"
        elif r.get("wildfire_occurrence") == 1: d_type = "Wildfire"
        elif r.get("landslide_occurrence") == 1: d_type = "Landslide"
        elif r.get("drought_occurrence") == 1: d_type = "Drought"
        elif r.get("tsunami_occurrence") == 1: d_type = "Tsunami"

        score = int(r.get("risk_score_0_100", 45))
        r_level = r.get("risk_level", "LOW")
        a_level = r.get("alert_level", "GREEN")

        if disaster_filter != "All" and d_type != disaster_filter:
            continue
        if risk_filter != "All" and r_level != risk_filter:
            continue

        markers.append({
            "lat": float(r["latitude"]),
            "lng": float(r["longitude"]),
            "location_name": str(r.get("location_name", "Location")),
            "country": str(r.get("country", "")),
            "state": str(r.get("state", "")),
            "disaster_type": d_type,
            "risk_score": score,
            "risk_level": r_level,
            "alert_level": a_level,
            "severity": int(r.get("severity_1_10", 5))
        })

    return jsonify({"markers": markers})

@app.route('/api/model-metrics', methods=['GET'])
def api_model_metrics():
    metrics_path = os.path.join(Config.MODELS_DIR, "model_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Metrics not generated yet. Train models first."}), 404

@app.route('/api/alerts', methods=['GET', 'POST'])
def api_alerts():
    if request.method == 'POST':
        data = request.get_json()
        AlertService.update_alert_status(data.get("id"), data.get("status"))
        return jsonify({"status": "success"})
    
    status = request.args.get("status")
    disaster_type = request.args.get("disaster")
    alerts = AlertService.get_alerts(status, disaster_type)
    return jsonify({"alerts": alerts})

@app.route('/api/history', methods=['GET'])
def api_history():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({"history": [dict(r) for r in rows]})

@app.route('/api/translations/<lang>', methods=['GET'])
def api_translations(lang):
    return jsonify(TRANSLATIONS.get(lang, TRANSLATIONS["en"]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)