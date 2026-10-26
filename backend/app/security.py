"""Minimal protective controls for a local demo. Not production IAM, rate limits or anti-bot."""
from __future__ import annotations
from collections import defaultdict, deque
from datetime import datetime, timezone
import hmac
import os
from threading import Lock
from time import monotonic
from fastapi import HTTPException, Request

_lock = Lock()
_times: dict[tuple[str, str], deque[float]] = defaultdict(deque)

def require_reporter_key(request: Request):
    configured = os.getenv("REPORTER_API_KEY", "")
    if configured and not hmac.compare_digest(request.headers.get("X-Reporter-Key", ""), configured):
        raise HTTPException(status_code=403, detail="Reporter access key required")

def rate_limit(request: Request, bucket: str, limit: int = 30, window_seconds: int = 3600):
    # Single-process guard, keyed by socket peer rather than X-Forwarded-For.
    # A shared Redis limiter and authenticated accounts are required at scale.
    addr = request.client.host if request.client else "unknown"
    key = (bucket, addr)
    now = monotonic()
    with _lock:
        dq = _times[key]
        while dq and now - dq[0] >= window_seconds:
            dq.popleft()
        if len(dq) >= limit:
            raise HTTPException(status_code=429, detail="Local request limit exceeded; retry later")
        dq.append(now)
        if len(_times) > 5000:
            _times.clear()

def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response
