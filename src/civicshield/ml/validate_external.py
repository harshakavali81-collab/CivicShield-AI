"""Reproducible experimental geographic AND chronological holdout validation.

Run only on legally sourced, independently labeled outcomes:
python -m civicshield.ml.validate_external --data path/to/labeled.csv --output report.json
This script cannot certify emergency readiness, and ships with NO validation data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    brier_score_loss, balanced_accuracy_score, confusion_matrix,
    precision_score, recall_score, f1_score, average_precision_score,
)
from civicshield.data_processing.features import FEATURE_COLUMNS

REQUIRED = ["observed_at", "district", "risk_label", *FEATURE_COLUMNS]

def _metric_report(model, features: pd.DataFrame) -> dict:
    if len(features) < 30 or features["risk_label"].nunique() != 2:
        raise ValueError("Each independent holdout needs >=30 observations and both classes")
    actual = features["risk_label"].astype(int).to_numpy()
    probabilities = model.predict_proba(features[FEATURE_COLUMNS])[:, 1]
    predicted = (probabilities >= 0.5).astype(int)
    npos = int(actual.sum())
    fn = int(((actual == 1) & (predicted == 0)).sum())
    return {
        "samples": len(actual), "events": npos,
        "balanced_accuracy": float(balanced_accuracy_score(actual, predicted)),
        "precision_positive": float(precision_score(actual, predicted, zero_division=0)),
        "recall_positive": float(recall_score(actual, predicted, zero_division=0)),
        "f1_positive": float(f1_score(actual, predicted, zero_division=0)),
        "false_negative_rate": float(fn / npos),
        "brier_score": float(brier_score_loss(actual, probabilities)),
        "average_precision": float(average_precision_score(actual, probabilities)),
        "confusion_matrix": confusion_matrix(actual, predicted, labels=[0, 1]).tolist(),
        "note": "Single held-out sample metrics; not generalizable safety guarantees.",
    }

def validate(csv_path: str, output: str, test_district: str | None = None) -> dict:
    path = Path(csv_path)
    frame = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    if len(frame) < 300:
        raise ValueError("At least 300 independently labeled rows required for this demo evaluation")
    frame["observed_at"] = pd.to_datetime(frame["observed_at"], utc=True, errors="raise")
    if frame[REQUIRED].isna().any().any():
        raise ValueError("Missing values require documented handling before evaluating")
    for key in FEATURE_COLUMNS:
        frame[key] = pd.to_numeric(frame[key], errors="raise")
        if not np.isfinite(frame[key]).all():
            raise ValueError("Features must be finite")
    if not frame["risk_label"].isin([0, 1]).all() or frame["risk_label"].nunique() < 2:
        raise ValueError("risk_label must have independently labeled binary outcomes 0 and 1")
    frame["district"] = frame["district"].astype(str).str.strip()
    districts = sorted(frame["district"].unique())
    if len(districts) < 3:
        raise ValueError("At least three geographic districts required")
    holdout_district = test_district or districts[-1]
    if holdout_district not in districts:
        raise ValueError("Chosen district is not in dataset")
    geographic = frame.loc[frame["district"] == holdout_district].copy()
    known = frame.loc[frame["district"] != holdout_district].copy()
    timestamps = sorted(known["observed_at"].unique())
    if len(timestamps) < 20:
        raise ValueError("Chronological evaluation needs >=20 distinct timestamps")
    boundary = timestamps[int(len(timestamps) * 0.8)]
    training = known.loc[known["observed_at"] < boundary]
    temporal = known.loc[known["observed_at"] >= boundary]
    if len(training) < 100 or training["risk_label"].nunique() != 2:
        raise ValueError("Insufficient training history/class coverage")
    # Fixed model hyperparameters; no tuning or feature-selection on either test group.
    model = RandomForestClassifier(n_estimators=120, max_depth=8, min_samples_leaf=4,
        class_weight="balanced", random_state=43, n_jobs=1)
    model.fit(training[FEATURE_COLUMNS], training["risk_label"].astype(int))
    report = {
        "status": "research_holdouts_only",
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "target_label": "risk_label (user-defined; independence not verifiable from file)",
        "features": FEATURE_COLUMNS,
        "heldout_district": holdout_district,
        "training_rows": len(training),
        "training_end_utc": training["observed_at"].max().isoformat(),
        "temporal_holdout_start_utc": temporal["observed_at"].min().isoformat(),
        "temporal_holdout": _metric_report(model, temporal),
        "geographic_holdout": _metric_report(model, geographic),
        "passes_operational_validation": False,
        "limitations": [
            "No proof of independently labeled real outcomes or adequate lead time.",
            "No validated storm-event independence, confidence intervals, calibration, expert evaluation or authority endorsement.",
            "District holdout choice is deterministic; repeat across districts and years.",
            "Never use metrics to make evacuation or emergency decisions.",
        ],
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="artifacts/evaluation_reports/external_validation.json")
    parser.add_argument("--test-district")
    args = parser.parse_args()
    report = validate(args.data, args.output, args.test_district)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
