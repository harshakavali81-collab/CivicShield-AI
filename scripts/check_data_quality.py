"""Offline historical labeled-data quality report (no internet, no emergency forecasts)."""
from __future__ import annotations
import argparse
import json
import pandas as pd
from civicshield.data_processing.features import FEATURE_COLUMNS

def audit(csv_path: str) -> dict:
    frame = pd.read_csv(csv_path)
    required = ["observed_at", "risk_label", *FEATURE_COLUMNS]
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        return {"status": "invalid", "missing_columns": missing}
    times = pd.to_datetime(frame["observed_at"], utc=True, errors="coerce")
    return {
        "status": "review_required",
        "total_rows": len(frame),
        "invalid_timestamp_count": int(times.isna().sum()),
        "duplicate_timestamp_count": int(times.duplicated().sum()),
        "feature_missing_counts": {key: int(frame[key].isna().sum()) for key in FEATURE_COLUMNS},
        "label_distribution": {str(key): int(value) for key, value in frame["risk_label"].value_counts(dropna=False).items()},
        "caveat": "Quality checks do not validate labels, leakage, independence or public safety fitness.",
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input_csv")
    args = p.parse_args()
    print(json.dumps(audit(args.input_csv), indent=2))

if __name__ == "__main__":
    main()
