"""Offline trust-boundary and response correlation regression checks."""
from __future__ import annotations
import re

import pytest
from backend.app.oidc import _configuration, _trusted_https_host

def test_oidc_keys_default_to_same_issuer_host(monkeypatch):
    monkeypatch.setenv("OIDC_ISSUER", "https://login.example.org/tenant")
    monkeypatch.setenv("OIDC_AUDIENCE", "civicshield-api")
    monkeypatch.setenv("OIDC_JWKS_URL", "https://login.example.org/tenant/keys")
    monkeypatch.delenv("OIDC_JWKS_ALLOWED_HOSTS", raising=False)
    assert _configuration()[2].endswith("/keys")
    monkeypatch.setenv("OIDC_JWKS_URL", "https://keys.example.org/jwks")
    with pytest.raises(RuntimeError, match="hostname"):
        _configuration()
    monkeypatch.setenv("OIDC_JWKS_ALLOWED_HOSTS", "keys.example.org")
    assert _configuration()[2] == "https://keys.example.org/jwks"

@pytest.mark.parametrize("url", (
    "http://auth.example.org/jwks",
    "https://localhost/jwks",
    "https://127.0.0.1/jwks",
    "https://192.168.1.1/jwks",
    "https://10.0.0.2/jwks",
    "https://169.254.169.254/jwks",
    "https://[::1]/keys",
    "https://private.internal/jwks",
    "https://user:password@auth.example.org/jwks",
    "https://auth.example.org:8000/jwks",
    "https://auth.example.org/jwks?token=secret",
    "https://auth.example.org/jwks#fragment",
    "https://intranet/keys",
    "https://auth.example.org/\nunsafe",
))
def test_rejects_unsafe_oidc_host(url):
    with pytest.raises(RuntimeError):
        _trusted_https_host(url, "OIDC_JWKS_URL")

def test_exact_alternate_host_required(monkeypatch):
    monkeypatch.setenv("OIDC_ISSUER", "https://issuer.example.org")
    monkeypatch.setenv("OIDC_AUDIENCE", "civicshield-api")
    monkeypatch.setenv("OIDC_JWKS_URL", "https://keys.example.org/jwks")
    monkeypatch.setenv("OIDC_JWKS_ALLOWED_HOSTS", "*.example.org")
    with pytest.raises(RuntimeError, match="exact DNS"):
        _configuration()

def test_request_id_generated_server_side_and_no_client_echo(client):
    first = client.get("/api/health", headers={"X-Request-ID": "injected-user-key"})
    second = client.get("/api/v1/alerts")
    one, two = first.headers["x-request-id"], second.headers["x-request-id"]
    assert re.fullmatch(r"[0-9a-f]{32}", one)
    assert one != two
    assert one != "injected-user-key"
    assert first.headers["cache-control"] == "no-store"
    assert first.headers["referrer-policy"] == "no-referrer"

def test_request_id_on_authentication_failure(client):
    response = client.get("/api/v1/incidents/review")
    assert response.status_code == 403
    assert re.fullmatch(r"[0-9a-f]{32}", response.headers["x-request-id"])
