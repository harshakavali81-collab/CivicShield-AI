"""Optional production OIDC bearer verification; fail closed on missing or invalid config.

Requires an actual trusted identity provider. This module does not create accounts,
issue tokens, or grant anyone the responder role.
"""
from __future__ import annotations
import os
from ipaddress import ip_address
from functools import lru_cache
from urllib.parse import urlsplit
import jwt
from fastapi import HTTPException, Request
from jwt import PyJWKClient

def oidc_enabled() -> bool:
    return os.getenv("AUTH_MODE", "demo_key").strip().lower() == "oidc"

def _trusted_https_host(url: str, name: str) -> str:
    """Reject accidental local network/JWKS targets before HTTP is attempted.

    This is *configuration validation*, not DNS rebinding protection. Deployments
    must also enforce HTTPS certificate verification and network egress policy.
    """
    if not url or any(ord(ch) < 32 or ord(ch) == 127 for ch in url):
        raise RuntimeError(f"{name} must be a trusted external HTTPS URL")
    try:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").rstrip(".").lower()
        port = parsed.port
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a valid HTTPS URL") from exc
    if (parsed.scheme != "https" or not host or not parsed.netloc
        or parsed.username is not None or parsed.password is not None
        or parsed.query or parsed.fragment or port not in (None, 443)):
        raise RuntimeError(f"{name} must be a trusted external HTTPS URL")
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        raise RuntimeError(f"{name} cannot target local services")
    try:
        address = ip_address(host)
    except ValueError:
        # Require an unambiguous hostname rather than a relative/intranet name.
        if "." not in host or host.startswith(".") or host.endswith("."):
            raise RuntimeError(f"{name} needs a public DNS hostname")
    else:
        if not address.is_global:
            raise RuntimeError(f"{name} cannot target a private or reserved IP address")
    return host


def _configuration() -> tuple[str, str, str]:
    issuer = os.getenv("OIDC_ISSUER", "").rstrip("/")
    audience = os.getenv("OIDC_AUDIENCE", "")
    jwks_url = os.getenv("OIDC_JWKS_URL", "")
    if not issuer or not audience or not jwks_url or audience.strip() != audience:
        raise RuntimeError("OIDC issuer, audience and JWKS endpoint are required")
    issuer_host = _trusted_https_host(issuer, "OIDC_ISSUER")
    jwks_host = _trusted_https_host(jwks_url, "OIDC_JWKS_URL")

    # Same-host keys are the typical OIDC arrangement. For separately hosted
    # signing keys, an operator must explicitly allow the precise hostname.
    alternate_hosts = {
        part.strip().lower()
        for part in os.getenv("OIDC_JWKS_ALLOWED_HOSTS", "").split(",")
        if part.strip()
    }
    if any("*" in host or "/" in host or ":" in host for host in alternate_hosts):
        raise RuntimeError("OIDC_JWKS_ALLOWED_HOSTS must use exact DNS hostnames")
    if jwks_host != issuer_host and jwks_host not in alternate_hosts:
        raise RuntimeError("JWKS hostname must match issuer or be explicitly allowed")
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
    for origin in origins:
        if "*" in origin:
            raise RuntimeError("Production needs explicit HTTPS CORS_ORIGINS")
        try:
            parsed = urlsplit(origin)
            acceptable = (
                parsed.scheme == "https" and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and parsed.path in ("", "/") and not parsed.query and not parsed.fragment
            )
        except ValueError:
            acceptable = False
        if not acceptable:
            raise RuntimeError("Production needs explicit HTTPS CORS_ORIGINS")
    if not origins:
        raise RuntimeError("Production needs explicit HTTPS CORS_ORIGINS")
