import os
import json
import requests
from config import Config

class AIService:
    @staticmethod
    def generate_explanation(disaster_type, location, probability, risk_score, risk_level, severity, top_factors):
        prompt = f"""
You are an AI disaster-risk communication assistant for DisasterAI.
Analyze the following machine learning model outputs for natural disaster prediction:

Disaster: {disaster_type}
Location: {location}
Probability: {probability}%
Risk Score: {risk_score}/100
Risk Level: {risk_level}
Severity: {severity}/10
Important Factors: {', '.join([f['feature'] for f in top_factors])}

Provide a concise, factual summary in JSON format with strictly these keys:
"explanation": A simple 2-sentence explanation of why the risk score is at this level based on factors.
"warning_message": A formal short warning message suitable for early alerts.
"recommendations": A list of exactly 3 practical safety/preparedness actions.

Rule: Never claim guaranteed occurrence. Use decision-support phrasing. Remind users to follow local official emergency channels.
"""
        # Call External AI API (Gemini / OpenAI API compatible structure) if key available
        if Config.AI_API_KEY:
            try:
                # Example using standard REST API call
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.AI_MODEL}:generateContent?key={Config.AI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }
                res = requests.post(url, json=payload, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return json.loads(text)
            except Exception as e:
                print(f"[AIService] API Request Failed, triggering fallback: {e}")

        # Deterministic Fallback Implementation
        factors_str = ", ".join([f['feature'].replace('_', ' ').title() for f in top_factors[:3]]) or "environmental indicators"
        return {
            "explanation": f"The ML model predicts a {risk_level.lower()} risk level ({risk_score}/100) for {disaster_type} near {location}. Key contributing factors include elevated readings in {factors_str}.",
            "warning_message": f"EARLY WARNING: Elevated {disaster_type} risk detected in {location}. Alert Level: {risk_level}.",
            "recommendations": [
                "Monitor local government and meteorological emergency bulletins continuously.",
                "Review disaster preparedness kits and ensure emergency contacts are accessible.",
                "Identify local safe zones and prepare for potential precautionary evacuation."
            ]
        }