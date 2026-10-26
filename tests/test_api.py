"""API contracts, incident handling, and authorization."""
def risk_payload(**overrides):
    value = {
        "city": "Hyderabad", "rainfall_24h_mm": 70,
        "temperature_c": 29, "humidity_pct": 85, "forecast_age_hours": 1,
    }
    value.update(overrides)
    return value

def incident_payload(**overrides):
    value = {
        "title": "Fallen tree blocking street",
        "description": "A fallen tree has blocked the public road near a bus stop.",
        "city": "Hyderabad", "language": "en",
    }
    value.update(overrides)
    return value

def test_health_and_sources(client):
    assert client.get("/api/health").json()["mode"] == "research_demo"
    assert client.get("/api/v1/sources").json()["automated_alert_ingestion"] is False

def test_sample_weather_is_explicitly_synthetic(client):
    response = client.get("/api/v1/weather/sample").json()
    assert response["source_type"] == "synthetic_demo"
    assert response["not_live_weather"] is True

def test_valid_risk_returns_not_official(client):
    response = client.post("/api/v1/risk/estimate", json=risk_payload())
    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "high"
    assert body["model_mode"] == "demonstration_heuristic"
    assert body["is_official_warning"] is False
    assert body["model_score"] is None

def test_stale_input_cannot_return_lower_risk(client):
    response = client.post("/api/v1/risk/estimate", json=risk_payload(rainfall_24h_mm=0, forecast_age_hours=7))
    assert response.status_code == 200
    assert response.json()["risk_level"] == "unavailable"
    assert response.json()["data_stale"] is True

def test_missing_and_invalid_inputs_rejected(client):
    assert client.post("/api/v1/risk/estimate", json=risk_payload(rainfall_24h_mm=-1)).status_code == 422
    assert client.post("/api/v1/risk/estimate", json={}).status_code == 422
    assert client.post("/api/v1/risk/estimate", json=risk_payload(unexpected="x")).status_code == 422

def test_official_alerts_never_fabricated(client):
    data = client.get("/api/v1/alerts").json()
    assert data["official_alerts"] == []
    assert data["connection_state"] == "not_connected"
    assert "does not mean" in data["message"]

def test_analytics_synthetic_vs_stored_provenance(client):
    assert client.get("/api/v1/analytics/summary").json()["report_total"] == 0
    assert client.get("/api/v1/analytics/trends").json()["not_real_events"] is True

def test_incident_submission_and_suggested_priority(client):
    response = client.post("/api/v1/incidents", json=incident_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["category"] == "fallen_tree"
    assert body["possible_duplicate"] is False
    assert "dispatch" in body["message"]

def test_exact_duplicate_flagged_but_not_suppressed(client):
    client.post("/api/v1/incidents", json=incident_payload())
    second = client.post("/api/v1/incidents", json=incident_payload()).json()
    assert second["possible_duplicate"] is True
    assert client.get("/api/v1/analytics/summary").json()["report_total"] == 2

def test_coordinate_validation(client):
    assert client.post("/api/v1/incidents", json=incident_payload(latitude=17.3)).status_code == 422
    assert client.post("/api/v1/incidents", json=incident_payload(latitude=95, longitude=78)).status_code == 422

def test_reports_disabled_by_default_when_not_opted_in(client, monkeypatch):
    monkeypatch.setenv("INCIDENT_SUBMISSIONS_ENABLED", "false")
    assert client.post("/api/v1/incidents", json=incident_payload()).status_code == 503

def test_reviewer_requires_a_key(client):
    assert client.get("/api/v1/incidents/review").status_code == 403
    assert client.get("/api/v1/incidents/review", headers={"X-Responder-Key": "wrong"}).status_code == 403

def test_reviewer_can_review_human_decision(client):
    identifier = client.post("/api/v1/incidents", json=incident_payload()).json()["id"]
    headers = {"X-Responder-Key": "test-only-review-key"}
    reports = client.get("/api/v1/incidents/review", headers=headers).json()["incidents"]
    assert reports[0]["id"] == identifier
    response = client.patch("/api/v1/incidents/" + identifier + "/review", headers=headers, json={
        "status": "verified", "reviewer_note": "Verified by demo reviewer"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "verified"

def test_contact_redaction_in_reviewer_queue(client):
    client.post("/api/v1/incidents", json=incident_payload(
        description="Please call 9876543210 or me@example.com about this fallen tree."
    ))
    queue = client.get("/api/v1/incidents/review", headers={"X-Responder-Key": "test-only-review-key"})
    text = queue.json()["incidents"][0]["description"]
    assert "9876543210" not in text
    assert "me@example.com" not in text
    assert "[phone redacted]" in text

def test_review_key_not_configured_disables_review(client, monkeypatch):
    monkeypatch.setenv("RESPONDER_API_KEY", "")
    assert client.get("/api/v1/incidents/review", headers={"X-Responder-Key": "anything"}).status_code == 503
