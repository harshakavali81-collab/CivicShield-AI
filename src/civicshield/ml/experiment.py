"""Optional MLflow experiment logging on evaluation JSON, no credentials in repository."""
from __future__ import annotations
import json
from pathlib import Path

def log_experiment(metrics_file: str, experiment_name: str = "civicshield-local") -> str:
    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError('Install pip install "civicshield-ai[tracking]"') from exc
    metrics = json.loads(Path(metrics_file).read_text(encoding="utf-8"))
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run() as run:
        mlflow.log_param("mode", metrics.get("mode", "unknown"))
        mlflow.log_param("split", metrics.get("split", "unknown"))
        mlflow.log_metric("balanced_accuracy", float(metrics["balanced_accuracy"]))
        mlflow.log_metric("train_samples", int(metrics["train_samples"]))
        mlflow.log_metric("holdout_samples", int(metrics["holdout_samples"]))
        mlflow.log_artifact(metrics_file)
        return run.info.run_id
