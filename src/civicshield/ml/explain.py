"""Optional post-training SHAP analysis; all results are experimental correlations."""
from __future__ import annotations
from pathlib import Path
import joblib
import pandas as pd
from civicshield.data_processing.features import FEATURE_COLUMNS

def explain(model_path: str, inputs: dict[str, float]) -> dict:
    try:
        import shap
    except ImportError as exc:
        raise RuntimeError('Install pip install "civicshield-ai[explain]"') from exc
    # Trusted local model only. joblib can execute arbitrary code when loaded.
    model = joblib.load(Path(model_path))
    values = pd.DataFrame([{key: float(inputs[key]) for key in FEATURE_COLUMNS}])
    forest = model.named_steps["model"]
    transformed = model.named_steps["impute"].transform(values)
    shap_values = shap.TreeExplainer(forest).shap_values(transformed)
    # sklearn binary classifier behavior across SHAP versions: list or ndarray.
    import numpy as np
    arr = np.asarray(shap_values)
    if isinstance(shap_values, list):
        contributions = np.asarray(shap_values[1])[0]
    elif arr.ndim == 3:
        contributions = arr[0, :, 1]
    else:
        contributions = arr[0]
    return {
        "model_mode": "user_trained_experimental",
        "contributions": {
            name: round(float(value), 5) for name, value in zip(FEATURE_COLUMNS, contributions)
        },
        "disclaimer": "SHAP contributions describe model behavior; they are not causal effects or safety evidence.",
    }
