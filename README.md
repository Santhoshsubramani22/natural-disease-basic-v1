
# 🌍 Natural Disaster Risk Prediction System

An AI-powered **Natural Disaster Risk Prediction and Early Warning System** built with Python, Flask, and Machine Learning.

The system analyzes environmental and geographical data to estimate the risk of natural disasters, generate risk scores, provide AI-assisted explanations and recommendations, and visualize prediction history, analytics, alerts, and disaster locations through a web dashboard.

> **Project:** `natural-disease-basic-v1`  
> **Version:** V1  
> **Backend:** Flask + Python  
> **Machine Learning:** Scikit-learn + XGBoost  
> **Database:** SQLite

---

## ✨ Features

### 🤖 Machine Learning Prediction

The system supports prediction for:

- 🌊 Flood
- 🌎 Earthquake
- 🌀 Cyclone
- 🔥 Wildfire
- ⛰️ Landslide
- ☀️ Drought
- 🌊 Tsunami

Multiple machine-learning algorithms are available:

- Random Forest
- Logistic Regression
- Decision Tree
- XGBoost

---

### 📊 Risk Scoring

Every prediction is converted into a **0–100 risk score**.

| Risk Score | Risk Level | Alert Level |
|---:|---|---|
| 0–24 | MINIMAL | 🟢 GREEN |
| 25–49 | LOW | 🟢 GREEN |
| 50–69 | MEDIUM | 🟠 ORANGE |
| 70–84 | HIGH | 🔴 RED |
| 85–100 | VERY HIGH | 🔴 RED |

The system also calculates a severity score from **1–10**.

---

### 🧠 AI-Assisted Explanations

The application can generate:

- Risk explanations
- Early-warning messages
- Safety recommendations
- Key contributing factors

If the AI API is unavailable, the application can use a fallback response.

---

### 🚨 Automatic Alerts

When a prediction reaches a risk score of **70 or higher**, the system automatically creates an alert.

Alerts are stored in the SQLite database and can be viewed through the alerts interface.

---

### 🗺️ Disaster Risk Map

The application provides a map interface for visualizing disaster-risk locations.

Map information includes:

- Latitude
- Longitude
- Location
- Country
- State
- Disaster type
- Risk score
- Risk level
- Alert level
- Severity

The map supports filtering by disaster type and risk level.

---

### 📈 Analytics Dashboard

The analytics dashboard provides information such as:

- Total dataset records
- Disaster occurrence counts
- Flood vs rainfall analysis
- Wildfire vs temperature analysis
- Cyclone vs wind-speed analysis
- Earthquake vs magnitude analysis

---

### 📋 Prediction History

Predictions are stored in SQLite.

History includes:

- Timestamp
- Disaster type
- Location
- Coordinates
- Probability
- Risk score
- Risk level
- Severity
- Alert level
- Model used
- AI-generated explanation

---

# 🏗️ Project Structure

```text
natural-disease-basic-v1/
│
├── app.py
├── config.py
├── requirements.txt
│
├── data/
│   └── natural_disaster_ml_dataset_5000.csv
│
├── database/
│   └── disaster.db
│
├── models/
│   ├── preprocessor.pkl
│   ├── model_metrics.json
│   ├── flood_random_forest.pkl
│   ├── flood_logistic_regression.pkl
│   ├── flood_decision_tree.pkl
│   ├── flood_xgboost.pkl
│   ├── earthquake_*.pkl
│   ├── cyclone_*.pkl
│   ├── wildfire_*.pkl
│   ├── landslide_*.pkl
│   ├── drought_*.pkl
│   └── tsunami_*.pkl
│
├── services/
│   ├── ai_service.py
│   ├── alert_service.py
│   ├── ml_service.py
│   └── translation_service.py
│
├── static/
│   └── ...
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── analytics.html
│   ├── models.html
│   ├── map.html
│   ├── alerts.html
│   └── history.html
│
├── training/
│   └── train_models.py
│
└── utils/
    └── ...
````

---

# 🔄 How It Works

```text
                    ┌─────────────────────┐
                    │     User Input      │
                    │ Environmental Data  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Data Preprocessing │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       ML Model Selection       │
              │                                │
              │ Random Forest / XGBoost /      │
              │ Logistic Regression /          │
              │ Decision Tree                  │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Probability / Risk │
                    │      Score 0–100     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ AI Explanation   │        │ Automatic Alert  │
       │ & Recommendations│        │ if Risk ≥ 70     │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Dashboard / History │
                    │ Analytics / Map     │
                    └─────────────────────┘
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Santhoshsubramani22/natural-disease-basic-v1.git
cd natural-disease-basic-v1
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies include:

* Flask
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Joblib
* Python-dotenv
* Requests

---

# ⚙️ Configuration

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your-secret-key

AI_API_KEY=your-ai-api-key
AI_MODEL=gemini-1.5-flash

GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### Environment Variables

| Variable              | Description                           | Required    |
| --------------------- | ------------------------------------- | ----------- |
| `FLASK_SECRET_KEY`    | Flask application secret key          | Recommended |
| `AI_API_KEY`          | API key for AI-generated explanations | Optional    |
| `AI_MODEL`            | AI model name                         | Optional    |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key                   | Optional    |

> **Important:** Never commit your `.env` file or API keys to GitHub.

---

# ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

Open the URL in your browser.

---

# 🖥️ Application Pages

| Page       | Route         | Description                   |
| ---------- | ------------- | ----------------------------- |
| Home       | `/`           | Main landing page             |
| Dashboard  | `/dashboard`  | Risk and prediction overview  |
| Prediction | `/prediction` | Generate disaster predictions |
| Analytics  | `/analytics`  | Dataset analytics             |
| Models     | `/models`     | ML model information          |
| Map        | `/map`        | Geographic risk visualization |
| Alerts     | `/alerts`     | View and manage alerts        |
| History    | `/history`    | Prediction history            |

---

# 🔌 API Reference

## Get Available Disasters and Algorithms

```http
GET /api/disasters
```

Returns the supported disaster types and ML algorithms.

Example:

```json
{
  "disasters": [
    "Flood",
    "Earthquake",
    "Cyclone",
    "Wildfire",
    "Landslide",
    "Drought",
    "Tsunami"
  ],
  "algorithms": [
    "random_forest",
    "logistic_regression",
    "decision_tree",
    "xgboost"
  ]
}
```

---

## Generate Prediction

```http
POST /api/predict
```

Example request:

```json
{
  "disaster_type": "Flood",
  "algorithm": "random_forest",
  "location_name": "Chennai",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "rainfall_24h_mm": 150,
  "humidity_percent": 85
}
```

Example response:

```json
{
  "prediction": "YES",
  "probability": 82.5,
  "risk_score": 83,
  "risk_level": "HIGH",
  "severity": 9,
  "alert_level": "RED",
  "disaster_type": "Flood",
  "algorithm": "random_forest"
}
```

---

## Dashboard Data

```http
GET /api/dashboard
```

Returns dashboard statistics including:

* Total predictions
* High-risk predictions
* Active alerts
* Average risk score
* Risk distribution
* Recent predictions

---

## Analytics

```http
GET /api/analytics
```

Returns dataset statistics and analytics information.

---

## Map Data

```http
GET /api/map-data
```

Optional filters:

```text
/api/map-data?disaster=Flood
/api/map-data?risk=HIGH
```

---

## Model Metrics

```http
GET /api/model-metrics
```

Returns available ML model performance metrics.

---

## Alerts

```http
GET /api/alerts
```

Optional filters:

```text
/api/alerts?status=Unread
/api/alerts?disaster=Flood
```

---

## Prediction History

```http
GET /api/history
```

Returns previously generated predictions.

---

# 🧠 Machine Learning

The system uses multiple machine-learning algorithms:

### Random Forest

An ensemble learning algorithm that combines multiple decision trees to improve prediction performance.

### Logistic Regression

A classification algorithm used to estimate the probability of disaster occurrence.

### Decision Tree

A tree-based classification algorithm that makes decisions using feature-based rules.

### XGBoost

A gradient-boosting algorithm designed for high-performance classification and prediction.

---

## Model Files

Trained models are stored in the `models/` directory.

Example:

```text
models/
├── preprocessor.pkl
├── model_metrics.json
├── flood_random_forest.pkl
├── flood_logistic_regression.pkl
├── flood_decision_tree.pkl
├── flood_xgboost.pkl
├── earthquake_random_forest.pkl
├── earthquake_logistic_regression.pkl
├── ...
```

---

# 🏋️ Training Models

The model training script is located at:

```text
training/train_models.py
```

To train the models:

```bash
python training/train_models.py
```

After training, the generated model files and metrics are stored in the `models/` directory.

> **Note:** Back up existing model files before retraining if you want to preserve the current models.

---

# 💾 Database

The project uses **SQLite** to store application data.

Database location:

```text
database/disaster.db
```

### Predictions Table

Stores information such as:

* Prediction timestamp
* Disaster type
* Location
* Coordinates
* Probability
* Risk score
* Risk level
* Severity
* Alert level
* Model used
* Explanation

### Alerts Table

Stores:

* Alert timestamp
* Disaster type
* Location
* Risk score
* Alert level
* Alert message
* Alert status

---

# 📁 Dataset

The main dataset is:

```text
data/natural_disaster_ml_dataset_5000.csv
```

The dataset is used for analytics and supports the project's natural-disaster prediction workflow.

---

# 🛠️ Technology Stack

| Category             | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Backend              | Flask                 |
| Machine Learning     | Scikit-learn          |
| ML Boosting          | XGBoost               |
| Data Processing      | Pandas, NumPy         |
| Model Serialization  | Joblib                |
| Database             | SQLite                |
| Frontend             | HTML, CSS, JavaScript |
| Templates            | Jinja2                |
| Maps                 | Google Maps API       |
| AI                   | Generative AI API     |

---

# 🔐 Security

Before deploying the application:

* Use a strong `FLASK_SECRET_KEY`.
* Never commit API keys.
* Keep `.env` out of version control.
* Restrict Google Maps API keys where possible.
* Use HTTPS in production.
* Validate user input.
* Use production-grade Flask deployment instead of the development server.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 🧪 Example Prediction Flow

```text
User selects disaster
        ↓
User selects ML algorithm
        ↓
User enters environmental data
        ↓
Data preprocessing
        ↓
ML model prediction
        ↓
Probability calculated
        ↓
Risk score generated
        ↓
Risk level determined
        ↓
AI explanation generated
        ↓
Prediction saved to database
        ↓
Alert generated if risk ≥ 70
        ↓
Result displayed on dashboard
```

---

# 📊 Risk Levels

```text
0 ───────────────────────────── 100
│
├── 0–24     MINIMAL
│
├── 25–49    LOW
│
├── 50–69    MEDIUM
│
├── 70–84    HIGH
│
└── 85–100   VERY HIGH
```

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Predict potential natural-disaster risks using machine learning.
2. Provide an easy-to-use web interface.
3. Calculate understandable risk scores.
4. Generate early-warning alerts for high-risk situations.
5. Visualize disaster risks geographically.
6. Store prediction history for analysis.
7. Provide analytics for disaster-related datasets.
8. Support AI-assisted explanations and safety recommendations.

---

# 🔮 Future Improvements

Possible future enhancements include:

* Real-time weather API integration
* Live earthquake feeds
* Satellite imagery analysis
* Deep-learning models
* IoT sensor integration
* SMS and email alerts
* Mobile application
* Real-time notification system
* More detailed geographic risk analysis
* Model explainability using SHAP
* Cloud deployment
* User authentication and role management

---

# ⚠️ Disclaimer

This project is intended for **educational, research, and demonstration purposes**.

Machine-learning predictions should not be treated as official disaster warnings or as a replacement for information from government agencies, meteorological departments, emergency services, or other authoritative sources.

For real-world emergency decisions, always follow official warnings and instructions from the relevant authorities.

---

# 👨‍💻 Author

**Santhosh Subramani**

GitHub:

```text
https://github.com/Santhoshsubramani22
```

Project:

```text
https://github.com/Santhoshsubramani22/natural-disease-basic-v1
```

---

# ⭐ Support

If you find this project useful:

⭐ Star the repository
🍴 Fork the project
🐛 Report issues
💡 Suggest improvements
🤝 Contribute to the project

---

## 📄 License

Add your preferred open-source license here, such as **MIT License**, if you intend to distribute the project under that license.

```
