import os
import sys
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Config
from utils.preprocessing import get_preprocessing_pipeline, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, get_feature_names

DISASTER_TARGET_MAP = {
    "flood": "flood_occurrence",
    "earthquake": "earthquake_occurrence",
    "cyclone": "cyclone_occurrence",
    "wildfire": "wildfire_occurrence",
    "landslide": "landslide_occurrence",
    "drought": "drought_occurrence",
    "tsunami": "tsunami_occurrence"
}

def train_all_models():
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    df = pd.read_csv(Config.DATASET_PATH)

    # Clean & Fit Preprocessor on complete feature space
    X_raw = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    preprocessor = get_preprocessing_pipeline()
    X_transformed = preprocessor.fit_transform(X_raw)
    
    # Save fitted preprocessor
    joblib.dump(preprocessor, os.path.join(Config.MODELS_DIR, "preprocessor.pkl"))
    
    feature_names = get_feature_names(preprocessor)
    all_metrics = {}

    for disaster_key, target_col in DISASTER_TARGET_MAP.items():
        print(f"--- Training Models for: {disaster_key.upper()} ---")
        y = df[target_col].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed, y, test_size=0.2, random_state=42, stratify=y
        )

        models = {
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
            "decision_tree": DecisionTreeClassifier(max_depth=8, random_state=42),
            "random_forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
            "xgboost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric='logloss')
        }

        all_metrics[disaster_key] = {}

        for algo_name, model in models.items():
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
            else:
                y_prob = y_pred

            # Metrics
            acc = float(accuracy_score(y_test, y_pred))
            prec = float(precision_score(y_test, y_pred, zero_division=0))
            rec = float(recall_score(y_test, y_pred, zero_division=0))
            f1 = float(f1_score(y_test, y_pred, zero_division=0))
            roc_auc = float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else 0.5
            
            cm = confusion_matrix(y_test, y_pred).tolist()
            fpr, tpr, _ = roc_curve(y_test, y_prob)

            # Feature Importance / Coeffs
            importances = []
            if algo_name in ["random_forest", "decision_tree", "xgboost"]:
                importances = model.feature_importances_.tolist()
            elif algo_name == "logistic_regression":
                importances = np.abs(model.coef_[0]).tolist()

            top_feat_idx = np.argsort(importances)[::-1][:10]
            top_features = [{"feature": feature_names[i], "importance": float(importances[i])} for i in top_feat_idx]

            # Save Model File
            model_filename = f"{disaster_key}_{algo_name}.pkl"
            joblib.dump(model, os.path.join(Config.MODELS_DIR, model_filename))

            # Store metrics
            all_metrics[disaster_key][algo_name] = {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(roc_auc, 4),
                "confusion_matrix": cm,
                "roc_curve": {"fpr": [round(x, 4) for x in fpr.tolist()], "tpr": [round(x, 4) for x in tpr.tolist()]},
                "top_features": top_features
            }

    # Save metrics JSON
    with open(os.path.join(Config.MODELS_DIR, "model_metrics.json"), "w") as f:
        json.dump(all_metrics, f, indent=4)

    print("\nTraining completed successfully! Preprocessor and models saved in models/")

if __name__ == "__main__":
    train_all_models()