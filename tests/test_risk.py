"""Safety gate and deliberate handling of model configuration."""
import pytest
from civicshield.incident_management.triage import categorize, duplicate_fingerprint, priority_hint
from civicshield.ml.predict import estimate_risk
from civicshield.monitoring.freshness import is_fresh

@pytest.mark.parametrize("age,expected", [(0, True), (6, True), (6.01, False), (24, False)])
def test_age_gate(age, expected):
    assert is_fresh(age) is expected

def test_heuristic_thresholds(monkeypatch):
    monkeypatch.delenv("CIVICSHIELD_MODEL_PATH", raising=False)
    assert estimate_risk(0, 25, 60, 1)["risk_level"] == "lower_indicator"
    assert estimate_risk(30, 25, 60, 1)["risk_level"] == "elevated"
    assert estimate_risk(65, 25, 60, 1)["risk_level"] == "high"
    assert estimate_risk(115, 25, 60, 1)["risk_level"] == "very_high"

def test_stale_always_unavailable():
    assert estimate_risk(0, 25, 60, 100)["risk_level"] == "unavailable"

def test_nonexistent_configured_model_never_silently_falls_back(monkeypatch):
    monkeypatch.setenv("CIVICSHIELD_MODEL_PATH", "/nonexistent/civicshield.joblib")
    with pytest.raises(FileNotFoundError):
        estimate_risk(100, 20, 70, 1)

def test_triage_and_dedup():
    assert categorize("Flooded road", "There is waterlogging") == "flooding"
    assert priority_hint("Help", "Person trapped and injured", "other") == "review_soon"
    assert duplicate_fingerprint("Tree fallen!", "Hyderabad", "fallen_tree") == duplicate_fingerprint(
        "tree fallen", "HYDERABAD", "fallen_tree"
    )
