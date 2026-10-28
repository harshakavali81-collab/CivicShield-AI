"""Pseudonymous reviewer references; avoid storing raw account subjects or emails.

Production requires a strong independent AUDIT_HASH_SECRET (not the IdP secret).
Changing this key breaks continuity of pseudonymous audit identifiers, so rotate
with a documented migration policy and never print or commit secrets.
"""
from __future__ import annotations

import hashlib
import hmac
import os

def actor_reference(claims: dict) -> str:
    issuer = claims.get("iss")
    subject = claims.get("sub")
    if not isinstance(issuer, str) or not isinstance(subject, str) or not issuer or not subject:
        return "local_demo_shared_key"
    key = os.getenv("AUDIT_HASH_SECRET", "")
    if os.getenv("APP_ENV", "local") == "production":
        if len(key) < 32:
            raise RuntimeError("Production audit pseudonym secret is missing or too short")
    else:
        # Safe only for artificial local test users; not a production pseudonym.
        key = key if len(key) >= 32 else "LOCAL_DEMO_ONLY_DO_NOT_USE_IN_PRODUCTION"
    data = (issuer + "\x00" + subject).encode("utf-8")
    return "oidc_" + hmac.new(key.encode("utf-8"), data, hashlib.sha256).hexdigest()[:56]
