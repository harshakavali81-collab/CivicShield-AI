"""Optional production OIDC bearer verification; fail closed on missing or invalid config.

Requires an actual trusted identity provider. This module does not create accounts,
issue tokens, or grant anyone the responder role.
"""
from __future__ import annotations
import os
from functools import lru_cache
from urllib.parse import urlparse
import jwt
from fastapi import HTTPException, Request
from jwt import PyJWKClient

def oidc_enabled() -> bool:
    return os.getenv("AUTH_MODE", "demo_key").strip().lower() == "oidc"

def _configuration() -> tuple[str, str, str]:
    issuer = os.getenv("OIDC_ISSUER", "").rstrip("/")
    audience = os.getenv("OIDC_AUDIENCE", "")
    jwks_url = os.getenv("OIDC_JWKS_URL", "")
    endpoints = (urlparse(issuer), urlparse(jwks_url))
    if (not all((issuer, audience, jwks_url))
        or any(p.scheme != "https" or not p.hostname or p.username or p.password for p in endpoints)
        or any(p.fragment or p.query for p in endpoints)):
        raise RuntimeError("OIDC requires issuer, audience, and HTTPS JWKS endpoint")
    return issuer, audience, jwks_url

@lru_cache(maxsize=8)
def _jwk_client(url: str) -> PyJWKClient:
    return PyJWKClient(url, cache_jwk_set=True, lifespan=300, timeout=5)

def validate_oidc_token(token: str) -> dict:
    issuer, audience, jwks_url = _configuration()
    if len(token) > 8192:
        raise ValueError("Token too large")
    key = _jwk_client(jwks_url).get_signing_key_from_jwt(token).key
    claims = jwt.decode(
        token, key, algorithms=["RS256"], audience=audience, issuer=issuer,
        options={"require": ["exp", "iat", "iss", "aud", "sub"]},
        leeway=30,
    )
    return claims

def _responder_role(claims: dict) -> bool:
    # Explicitly configured role membership, no implicit admin/user trust.
    claim_name = os.getenv("OIDC_ROLES_CLAIM", "roles")
    value = claims.get(claim_name, [])
    roles = [value] if isinstance(value, str) else value
    required = os.getenv("OIDC_RESPONDER_ROLE", "civicshield-responder")
    return isinstance(roles, list) and required in roles

def require_oidc_reviewer(request: Request) -> dict:
    header = request.headers.get("authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Bearer token required", headers={"WWW-Authenticate": "Bearer"})
    try:
        claims = validate_oidc_token(token)
    except (jwt.PyJWTError, ValueError, RuntimeError, OSError) as exc:
        raise HTTPException(status_code=401, detail="Invalid or unavailable identity token") from exc
    if not _responder_role(claims):
        raise HTTPException(status_code=403, detail="Responder role required")
    return claims

def validate_production_configuration() -> None:
    if os.getenv("APP_ENV", "local") != "production":
        return
    if not oidc_enabled():
        raise RuntimeError("Production must use OIDC authentication")
    _configuration()
    if not os.getenv("DATABASE_URL", "").startswith("postgresql"):
        raise RuntimeError("Production requires external PostgreSQL")
    if os.getenv("INCIDENT_SUBMISSIONS_ENABLED", "false").lower() == "true":
        raise RuntimeError("Public incident intake cannot be enabled by this demo's production config")
    audit_secret = os.getenv("AUDIT_HASH_SECRET", "")
    if len(audit_secret) < 32:
        raise RuntimeError("Production AUDIT_HASH_SECRET must have at least 32 characters")
    origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "").split(",") if value.strip()]
    if not origins or any(not item.startswith("https://") or "*" in item for item in origins):
        raise RuntimeError("Production needs explicit HTTPS CORS_ORIGINS")
