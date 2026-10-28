"""Bounded single-process demo rate limiter: no full-table bypass.

Not evidence of production protection: reverse proxies, shared Redis and
distributed clients require separately engineered enforcement.
"""
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from backend.app import security


@pytest.fixture(autouse=True)
def clean_limiter():
    with security._lock:
        security._times.clear()
    yield
    with security._lock:
        security._times.clear()


def client(host: str, forwarded_for: str = ""):
    return SimpleNamespace(
        client=SimpleNamespace(host=host),
        headers={"x-forwarded-for": forwarded_for},
    )


def test_exhaustion_never_clears_existing_limits(monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(security, "monotonic", lambda: clock[0])
    monkeypatch.setattr(security, "MAX_RATE_LIMIT_KEYS", 2)
    a, b, c = client("192.0.2.1"), client("192.0.2.2"), client("192.0.2.3")
    security.rate_limit(a, "demo", limit=1, window_seconds=60)
    security.rate_limit(b, "demo", limit=1, window_seconds=60)
    with pytest.raises(HTTPException) as overflow:
        security.rate_limit(c, "demo", limit=1, window_seconds=60)
    assert overflow.value.status_code == 429
    assert overflow.value.headers["Retry-After"] == "60"
    assert len(security._times) == 2
    with pytest.raises(HTTPException) as repeat:
        security.rate_limit(a, "demo", limit=1, window_seconds=60)
    assert repeat.value.status_code == 429
    assert len(security._times) == 2


def test_expired_keys_reclaimed_without_resetting_live_client(monkeypatch):
    clock = [200.0]
    monkeypatch.setattr(security, "monotonic", lambda: clock[0])
    monkeypatch.setattr(security, "MAX_RATE_LIMIT_KEYS", 2)
    a, b, c = client("alpha.example"), client("beta.example"), client("gamma.example")
    security.rate_limit(a, "lookup", limit=1, window_seconds=10)
    security.rate_limit(b, "lookup", limit=1, window_seconds=120)
    clock[0] = 211.0
    security.rate_limit(c, "lookup", limit=1, window_seconds=20)
    assert ("lookup", "alpha.example") not in security._times
    assert ("lookup", "beta.example") in security._times
    with pytest.raises(HTTPException) as err:
        security.rate_limit(b, "lookup", limit=1, window_seconds=120)
    assert err.value.status_code == 429
    assert int(err.value.headers["Retry-After"]) == 109


def test_differing_windows_prune_any_expired_deadlines(monkeypatch):
    clock = [1.0]
    monkeypatch.setattr(security, "monotonic", lambda: clock[0])
    user = client("same-client")
    security.rate_limit(user, "forecast", limit=2, window_seconds=120)
    security.rate_limit(user, "forecast", limit=2, window_seconds=10)
    clock[0] = 12.0
    security.rate_limit(user, "forecast", limit=2, window_seconds=15)
    assert len(security._times["forecast", "same-client"]) == 2
    with pytest.raises(HTTPException) as err:
        security.rate_limit(user, "forecast", limit=2, window_seconds=15)
    assert err.value.headers["Retry-After"] == "15"


def test_spoofed_forwarded_for_cannot_reset_socket_peer_quota(monkeypatch):
    monkeypatch.setattr(security, "monotonic", lambda: 300.0)
    security.rate_limit(client("shared-proxy", "1.1.1.1"), "lookup", limit=1)
    with pytest.raises(HTTPException) as err:
        security.rate_limit(client("shared-proxy", "8.8.8.8"), "lookup", limit=1)
    assert err.value.status_code == 429


@pytest.mark.parametrize("limit,window", [(0, 3600), (1, 0), (-1, 10), (2, -1)])
def test_invalid_quotas_rejected(limit, window):
    with pytest.raises(ValueError):
        security.rate_limit(client("any"), "bad", limit=limit, window_seconds=window)


def test_limits_protect_actual_api_endpoint(client, monkeypatch):
    monkeypatch.setenv("OPEN_METEO_ENABLED", "true")
    monkeypatch.setattr(security, "monotonic", lambda: 900.0)
    from backend.app import main
    async def fake_source(lat, lon):
        return {"source_type": "synthetic_test", "is_official_warning": False}
    monkeypatch.setattr(main, "fetch_weather", fake_source)
    with monkeypatch.context() as context:
        context.setattr(main, "rate_limit", lambda request, bucket, **kw:
            security.rate_limit(request, bucket, limit=1, window_seconds=60))
        first = client.get("/api/v1/weather/live?latitude=17.3&longitude=78.4")
        second = client.get("/api/v1/weather/live?latitude=17.3&longitude=78.4")
    assert first.status_code == 200
    assert second.status_code == 429
    assert second.headers["retry-after"] == "60"
    assert first.headers["x-request-id"] != second.headers["x-request-id"]
