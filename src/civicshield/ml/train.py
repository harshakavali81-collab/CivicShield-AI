"""Optional supervised experiment on OWN REAL labeled data; NEVER on generated demo labels."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import balanced_accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from civicshield.data_processing.features import FEATURE_COLUMNS

def train(data_path: str, output_path: str) -> dict:
    path = Path(data_path)
    frame = pd.read_csv(path)
    required = ["observed_at", "risk_label", *FEATURE_COLUMNS]
    missing = [key for key in required if key not in frame.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if len(frame) < 50:
        raise ValueError("At least 50 labeled observations required for a demo holdout")
    frame["observed_at"] = pd.to_datetime(frame["observed_at"], utc=True, errors="raise")
    if frame["observed_at"].duplicated().any():
        raise ValueError("Duplicate timestamps require explicit deduplication before training")
    for column in FEATURE_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
        if frame[column].isna().any():
            raise ValueError("Missing feature: " + column)
    if set(frame["risk_label"].dropna().unique()) != {0, 1}:
        raise ValueError("risk_label must contain binary integer labels 0 and 1")
    frame = frame.sort_values("observed_at").reset_index(drop=True)
    cut = int(len(frame) * 0.8)
    training, holdout = frame.iloc[:cut], frame.iloc[cut:]
    if training["risk_label"].nunique() != 2 or holdout["risk_label"].nunique() != 2:
        raise ValueError("Both chronological splits must have both classes")
    pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(
            n_estimators=100, min_samples_leaf=3, class_weight="balanced",
            random_state=42, n_jobs=1,
        )),
    ])
    pipeline.fit(training[FEATURE_COLUMNS], training["risk_label"].astype(int))
    y_true = holdout["risk_label"].astype(int)
    y_pred = pipeline.predict(holdout[FEATURE_COLUMNS])
    metrics = {
        "mode": "experimental_research",
        "train_samples": len(training), "holdout_samples": len(holdout),
        "split": "chronological_80_20",
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "input_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "warning": "Metrics on one holdout do not establish geographic transfer, calibration or safety.",
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output)
    output.with_suffix(".metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="artifacts/models/risk_model.joblib")
    args = parser.parse_args()
    print(json.dumps(train(args.data, args.output), indent=2))

if __name__ == "__main__":
    main()
