"""Chronological ML experiments: accepted and rejected training conditions."""
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytest
from civicshield.ml.train import train

def write_labeled(path, count=60, same_label=False):
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    records = [
        {
            "observed_at": (start + timedelta(days=i)).isoformat(),
            "rainfall_24h_mm": 20 + (i % 7) * 10,
            "temperature_c": 25 + i % 6,
            "humidity_pct": 60 + i % 10,
            "risk_label": 0 if same_label else i % 2,
        } for i in range(count)
    ]
    pd.DataFrame(records).to_csv(path, index=False)

def test_training_produces_metrics_and_artifact(tmp_path):
    path = tmp_path / "owned_labeled.csv"
    output = tmp_path / "model.joblib"
    write_labeled(path)
    metrics = train(str(path), str(output))
    assert output.is_file()
    assert output.with_suffix(".metrics.json").is_file()
    assert metrics["split"] == "chronological_80_20"
    assert metrics["holdout_samples"] == 12
    assert metrics["mode"] == "experimental_research"

def test_training_refuses_unlabeled_and_small_data(tmp_path):
    path = tmp_path / "small.csv"
    write_labeled(path, count=10)
    with pytest.raises(ValueError, match="50"):
        train(str(path), str(tmp_path / "out.joblib"))

def test_training_refuses_single_class(tmp_path):
    path = tmp_path / "oneclass.csv"
    write_labeled(path, same_label=True)
    with pytest.raises(ValueError, match="binary"):
        train(str(path), str(tmp_path / "out.joblib"))
