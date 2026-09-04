import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "disaster_ai_default_secret_key_2026")
    DATASET_PATH = os.path.join(BASE_DIR, "data", "natural_disaster_ml_dataset_5000.csv")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "disaster.db")
    
    # AI Credentials
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "gemini-1.5-flash")
    
    # Maps
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # Configurable Disaster Types
    DISASTER_TYPES = [
        "Flood", "Earthquake", "Cyclone", "Wildfire", 
        "Landslide", "Drought", "Tsunami"
    ]

    # Model Choices
    ALGORITHMS = [
        "random_forest", "logistic_regression", "decision_tree", "xgboost"
    ]

    # Risk Score Thresholds (0-100)
    RISK_LEVEL_THRESHOLDS = {
        "MINIMAL": (0, 24),
        "LOW": (25, 49),
        "MEDIUM": (50, 69),
        "HIGH": (70, 84),
        "VERY HIGH": (85, 100)
    }

    # Alert Level Thresholds
    ALERT_LEVEL_THRESHOLDS = {
        "GREEN": (0, 24),
        "YELLOW": (25, 49),
        "ORANGE": (50, 69),
        "RED": (70, 100)
    }