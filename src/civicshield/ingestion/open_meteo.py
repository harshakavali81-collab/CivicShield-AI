"""Non-authoritative modeled weather feed, independent of government warning sources.

Source: https://open-meteo.com/en/docs
Open-Meteo CC BY 4.0 data requires attribution. Free endpoint is noncommercial only.
This client returns modeled conditions, NEVER ground truth or an emergency warning.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from time import monotonic
import httpx

URL = "https://api.open-meteo.com/v1/forecast"
SOURCE_URL = "https://open-meteo.com/"
_LICENSE = "https://creativecommons.org/licenses/by/4.0/"
CACHE_TTL_SECONDS = 600
_cache: dict[tuple[float, float], tuple[float, dict]] = {}
_lock = asyncio.Lock()

def _utc(value: str) -> datetime:
    """Open-Meteo timezone=UTC strings are naive ISO8601 in UTC."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)

def normalize(payload: dict, latitude: float, longitude: float) -> dict:
    """Fail closed when provider arrays are absent, inconsistent or stale."""
    current = payload.get("current")
    hourly = payload.get("hourly")
    if not isinstance(current, dict) or not isinstance(hourly, dict):
        raise ValueError("Provider response lacks current/hourly fields")
    observed_at = _utc(current["time"])
    now = datetime.now(timezone.utc)
    age_hours = max(0, (now - observed_at).total_seconds() / 3600)
    if observed_at > now + timedelta(hours=1) or age_hours > 6:
        raise ValueError("Provider timestamp missing a recent valid period")
    times = hourly.get("time")
    rain = hourly.get("precipitation")
    if not isinstance(times, list) or not isinstance(rain, list) or len(times) != len(rain):
        raise ValueError("Hourly precipitation array is invalid")
    begin = observed_at - timedelta(hours=24)
    pairs = [
        float(amount)
        for value, amount in zip(times, rain)
        if begin < _utc(value) <= observed_at and amount is not None
    ]
    # Need enough hourly periods, never substitute zero when data is absent.
    if len(pairs) < 20 or any(p < 0 or p > 500 for p in pairs):
        raise ValueError("Insufficient trustworthy hourly precipitation coverage")
    temp = float(current["temperature_2m"])
    humidity = float(current["relative_humidity_2m"])
    if not (-40 <= temp <= 65 and 0 <= humidity <= 100):
        raise ValueError("Invalid current values")
    return {
        "latitude_approx": latitude,
        "longitude_approx": longitude,
        "temperature_c": round(temp, 1),
        "humidity_pct": round(humidity, 1),
        "modeled_precipitation_24h_mm": round(sum(pairs), 2),
        "source_timestamp_utc": observed_at.isoformat(),
        "retrieved_at_utc": now.isoformat(),
        "age_hours": round(age_hours, 2),
        "source_type": "third_party_modeled_weather",
        "provider": "Open-Meteo",
        "provider_url": SOURCE_URL,
        "license_url": _LICENSE,
        "is_official_warning": False,
        "is_ground_observation": False,
        "note": "Modeled gridded weather; not a station measurement, government alert or validated flood indicator.",
    }

async def fetch_weather(latitude: float, longitude: float) -> dict:
    # Coarsen request coordinates to ~1 km to minimize unnecessary precision sent to vendor.
    latitude, longitude = round(latitude, 2), round(longitude, 2)
    key = (latitude, longitude)
    async with _lock:
        cached = _cache.get(key)
        if cached and monotonic() - cached[0] < CACHE_TTL_SECONDS:
            return {**cached[1], "cache_hit": True}
    params = {
        "latitude": latitude, "longitude": longitude, "timezone": "UTC",
        "current": "temperature_2m,relative_humidity_2m",
        "hourly": "precipitation",
        "past_days": 2, "forecast_days": 1,
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(8.0), follow_redirects=False) as client:
        response = await client.get(URL, params=params)
        response.raise_for_status()
        result = normalize(response.json(), latitude, longitude)
    async with _lock:
        _cache[key] = (monotonic(), result)
        # Prevent indefinitely growing memory in a busy demo.
        if len(_cache) > 200:
            _cache.clear()
            _cache[key] = (monotonic(), result)
    return {**result, "cache_hit": False}
