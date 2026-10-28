"""Minimal protective controls for a local demo. Not production IAM, rate limits or anti-bot."""
from __future__ import annotations
from collections import defaultdict, deque
import hmac
import os
from uuid import uuid4
from threading import Lock
from time import monotonic
from math import ceil
from fastapi import HTTPException, Request

_lock = Lock()
# A bounded in-process demo limiter. Deque values are monotonic *expiry* times,
# preserving each entry's original window even when callers use different windows.
# This is not a distributed production traffic-control system.
MAX_RATE_LIMIT_KEYS = 5000
_times: dict[tuple[str, str], deque[float]] = defaultdict(deque)

def require_reporter_key(request: Request):
    configured = os.getenv("REPORTER_API_KEY", "")
    if configured and not hmac.compare_digest(request.headers.get("X-Reporter-Key", ""), configured):
        raise HTTPException(status_code=403, detail="Reporter access key required")

def _prune_expired(now: float) -> None:
    """Remove only expired entries, preserving active client quotas.

    Must be called with _lock held. We scan when capacity is reached rather
    than on every request, avoiding normal-path O(N) work.
    """
    for key, expires in tuple(_times.items()):
        active = [deadline for deadline in expires if deadline > now]
        if active:
            expires.clear()
            expires.extend(active)
        else:
            del _times[key]


def rate_limit(request: Request, bucket: str, limit: int = 30, window_seconds: int = 3600):
    """Best-effort local per-socket guard, never a public security boundary.

    Ignore untrusted X-Forwarded-For. A shared reverse-proxy socket can cause
    users to share a quota; real hosting needs authenticated identities and a
    shared datastore/edge limiter. At capacity reject new keys instead of
    clearing existing histories and granting fresh request allowances.
    """
    if limit < 1 or window_seconds < 1:
        raise ValueError("Rate-limit configuration must be positive")
    address = request.client.host if request.client else "unknown"
    key = (bucket, address)
    now = monotonic()
    with _lock:
        if key not in _times and len(_times) >= MAX_RATE_LIMIT_KEYS:
            _prune_expired(now)
            if len(_times) >= MAX_RATE_LIMIT_KEYS:
                raise HTTPException(
                    status_code=429,
                    detail="Demo rate-limit capacity reached; retry later",
                    headers={"Retry-After": "60"},
                )
        expires = _times[key]
        # A demo extension might use differing windows on one key. Expiry
        # order is not guaranteed in that case: retain all active deadlines.
        active = [deadline for deadline in expires if deadline > now]
        expires.clear()
        expires.extend(active)
        if len(expires) >= limit:
            retry_after = max(1, ceil(min(expires) - now))
            raise HTTPException(
                status_code=429,
                detail="Local request limit exceeded; retry later",
                headers={"Retry-After": str(retry_after)},
            )
        expires.append(now + window_seconds)


def security_headers(response):
    # Fresh random correlation value, never copied from untrusted client input.
    # No headers, tokens, incident narratives or locations are logged here.
    response.headers["X-Request-ID"] = uuid4().hex
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response
