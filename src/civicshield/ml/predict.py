"""Explicitly experimental risk estimates: heuristic demo or opt-in local supervised model."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd
from civicshield.data_processing.features import feature_record
from civicshield.monitoring.freshness import is_fresh

@lru_cache(maxsize=2)
def _trusted_local_model(path: str):
    # joblib/pickle files execute code when loaded. NEVER load user uploads or untrusted artifacts.
    if not Path(path).is_file():
        raise FileNotFoundError("Configured local model artifact is missing")
    return joblib.load(path)

def estimate_risk(rainfall: float, temp: float, humidity: float, age: float) -> dict:
    if not is_fresh(age):
        return {
            "risk_level": "unavailable", "data_stale": True, "model_mode": "none",
            "model_score": None, "explanation": [
                "Input is older than six hours; no risk estimate is available.",
                "Missing or stale data must never be interpreted as safety.",
            ],
        }
    path = os.getenv("CIVICSHIELD_MODEL_PATH", "").strip()
    if path:
        model = _trusted_local_model(path)
        record = feature_record(rainfall, temp, humidity)
        probability = float(model.predict_proba(pd.DataFrame([record]))[0][1])
        return {
            "risk_level": "higher_indicator" if probability >= 0.5 else "lower_indicator",
            "data_stale": False, "model_mode": "user_trained_experimental",
            "model_score": round(probability, 4),
            "explanation": [
                "Score from a locally configured, user-trained binary classifier.",
                "Score is not calibrated and is not an official hazard probability.",
                "Use independent validation and an official source for real decisions.",
            ],
        }
    if rainfall >= 115:
        level = "very_high"
    elif rainfall >= 65:
        level = "high"
    elif rainfall >= 30:
        level = "elevated"
    else:
        level = "lower_indicator"
    return {
        "risk_level": level, "data_stale": False, "model_mode": "demonstration_heuristic",
        "model_score": None,
        "explanation": [
            "Illustrative rainfall threshold grouping only; not a flood forecast.",
            "Temperature and humidity are accepted for model compatibility but are not used by the demo rule.",
            "Geography, river levels, drainage and uncertainties are not captured.",
            "Even a lower indicator does NOT mean an area is safe.",
        ],
    }
