import sqlite3
from config import Config

class AlertService:
    @staticmethod
    def create_alert(disaster_type, location, risk_score, alert_level, message):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (disaster_type, location, risk_score, alert_level, message, status)
            VALUES (?, ?, ?, ?, ?, 'Unread')
        """, (disaster_type, location, risk_score, alert_level, message))
        conn.commit()
        alert_id = cursor.lastrowid
        conn.close()
        return alert_id

    @staticmethod
    def get_alerts(status=None, disaster_type=None):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if disaster_type and disaster_type != "All":
            query += " AND disaster_type = ?"
            params.append(disaster_type)
            
        query += " ORDER BY timestamp DESC LIMIT 50"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update_alert_status(alert_id, status):
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE alerts SET status = ? WHERE id = ?", (status, alert_id))
        conn.commit()
        conn.close()