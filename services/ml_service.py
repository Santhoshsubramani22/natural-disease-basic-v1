import os
import json
import joblib
import numpy as np
import pandas as pd
from config import Config
from utils.preprocessing import NUMERICAL_FEATURES, CATEGORICAL_FEATURES, get_feature_names

class MLService:
    def __init__(self):
        self.models = {}
        self.preprocessor = None
        self.metrics = {}
        self.load_all()

    def load_all(self):
        prep_path = os.path.join(Config.MODELS_DIR, "preprocessor.pkl")
        if os.path.exists(prep_path):
            self.preprocessor = joblib.load(prep_path)

        metrics_path = os.path.join(Config.MODELS_DIR, "model_metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)

    def get_model(self, disaster_type, algorithm="random_forest"):
        d_key = disaster_type.lower()
        key = f"{d_key}_{algorithm}"
        if key not in self.models:
            path = os.path.join(Config.MODELS_DIR, f"{key}.pkl")
            if os.path.exists(path):
                self.models[key] = joblib.load(path)
            else:
                raise FileNotFoundError(f"Model file {path} not found. Please train models first.")
        return self.models[key]

    def predict(self, input_dict, disaster_type, algorithm="random_forest"):
        d_key = disaster_type.lower()
        model = self.get_model(d_key, algorithm)

        # Build single row dataframe with default fallback for missing dataset values
        row = {}
        for col in NUMERICAL_FEATURES:
            row[col] = float(input_dict.get(col, 0.0))
        for col in CATEGORICAL_FEATURES:
            row[col] = str(input_dict.get(col, "None"))

        df_input = pd.DataFrame([row])
        X_trans = self.preprocessor.transform(df_input)

        prob = float(model.predict_proba(X_trans)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(X_trans)[0])
        pred_label = "YES" if prob >= 0.5 else "NO"

        # Risk Score (0 - 100)
        risk_score = int(round(prob * 100))

        # Risk Level & Alert Level
        risk_level = "MINIMAL"
        for level, (low, high) in Config.RISK_LEVEL_THRESHOLDS.items():
            if low <= risk_score <= high:
                risk_level = level
                break

        alert_level = "GREEN"
        for level, (low, high) in Config.ALERT_LEVEL_THRESHOLDS.items():
            if low <= risk_score <= high:
                alert_level = level
                break

        # Severity 1-10
        severity = min(10, max(1, int(np.ceil(risk_score / 10.0))))

        # Calculate instance top factor impacts
        feature_names = get_feature_names(self.preprocessor)
        importances = []
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "coef_"):
            importances = np.abs(model.coef_[0])

        top_factors = []
        if len(importances) == len(feature_names):
            # Weigh feature by input standardized presence
            x_vec = X_trans[0]
            impacts = np.abs(x_vec * importances)
            top_idx = np.argsort(impacts)[::-1][:5]
            for idx in top_idx:
                fname = feature_names[idx].replace("num__", "").replace("cat__", "")
                top_factors.append({
                    "feature": fname,
                    "importance": float(importances[idx]),
                    "score": float(impacts[idx])
                })

        return {
            "prediction": pred_label,
            "probability": round(prob * 100, 2),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "severity": severity,
            "alert_level": alert_level,
            "disaster_type": disaster_type,
            "algorithm": algorithm,
            "top_factors": top_factors
        }

ml_service = MLService()