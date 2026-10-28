"""Optimistic review status locking for demo report moderation.

A stale dashboard cannot silently overwrite another human review decision.
This does not assert that the review is an official emergency verification.
"""
from backend.app.db import SessionLocal, ReviewAudit
from sqlalchemy import select, func

KEY = {"X-Responder-Key": "test-only-review-key"}

def payload():
    return {
        "title": "Tree blocking the training road",
        "description": "Fictional report for local review conflict tests only.",
        "city": "Fictional City",
    }

def test_stale_review_request_returns_conflict_and_does_not_write_audit(client):
    identifier = client.post("/api/v1/incidents", json=payload()).json()["id"]
    one = client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY, json={
        "status": "verified", "expected_status": "pending",
        "reviewer_note": "First local reviewer decision",
    })
    assert one.status_code == 200
    two = client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY, json={
        "status": "dismissed", "expected_status": "pending",
        "reviewer_note": "Stale browser tab decision",
    })
    assert two.status_code == 409
    assert "reload" in two.json()["detail"].lower()
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(ReviewAudit)) == 1
    queue = client.get("/api/v1/incidents/review", headers=KEY).json()["incidents"]
    assert queue[0]["status"] == "verified"

def test_review_can_continue_after_reloading_latest_status(client):
    identifier = client.post("/api/v1/incidents", json=payload()).json()["id"]
    assert client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY,
        json={"status": "needs_info", "expected_status": "pending"}).status_code == 200
    response = client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY,
        json={"status": "verified", "expected_status": "needs_info"})
    assert response.status_code == 200
    events = client.get("/api/v1/incidents/audit", headers=KEY).json()["events"]
    assert len(events) == 2
    assert {e["previous_status"] for e in events} == {"pending", "needs_info"}
    assert {e["new_status"] for e in events} == {"verified", "needs_info"}

def test_legacy_review_request_still_supported(client):
    identifier = client.post("/api/v1/incidents", json=payload()).json()["id"]
    response = client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY,
        json={"status": "verified"})
    assert response.status_code == 200

def test_invalid_expected_status_rejected(client):
    identifier = client.post("/api/v1/incidents", json=payload()).json()["id"]
    response = client.patch(f"/api/v1/incidents/{identifier}/review", headers=KEY,
        json={"status": "dismissed", "expected_status": "officially_verified"})
    assert response.status_code == 422
