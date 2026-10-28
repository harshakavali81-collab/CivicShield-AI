"""No email or raw OIDC subject is stored in review history."""
from __future__ import annotations
import hashlib

def actor_reference(claims: dict) -> str:
    issuer = claims.get("iss")
    subject = claims.get("sub")
    if isinstance(issuer, str) and isinstance(subject, str) and issuer and subject:
        # Salt/secret management and cross-record linkability should be reviewed
        # before processing personal records in a real operational system.
        return "oidc_" + hashlib.sha256((issuer + "\x00" + subject).encode("utf-8")).hexdigest()[:56]
    return "local_demo_shared_key"
