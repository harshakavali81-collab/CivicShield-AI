"""Run the same safe smoke test used by portfolio users against the in-process API."""
from scripts.smoke_demo import smoke

def test_smoke_demo_read_only_and_explicitly_non_authoritative(client):
    result = smoke(client)
    assert result["checks"] == 7
    assert result["status"] == "software_demo_smoke_passed"
    assert result["reports_submitted"] == 0
    assert result["live_government_feed_verified"] is False
    assert result["validated_emergency_prediction"] is False
