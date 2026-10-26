"""IMD district-warning adapter for licensed/authorized access only.

Documentation: https://api.imd.gov.in/public/api_reference.html
No API request is issued until IMD_API_ENABLED=true; failures must never be
silently represented as 'no warning'. Retain original IMD URL/timestamp.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
import os
import httpx

IMD_HOST = "api.imd.gov.in"
DISTRICT_WARNINGS = "https://api.imd.gov.in/api/v1/districtwarning"
DOCUMENTATION_URL = "https://api.imd.gov.in/public/api_reference.html"
ISSUE_MAX_AGE_HOURS = 36
COLOR = {1: "red", 2: "orange", 3: "yellow", 4: "green"}
CODES = {
    1: "no warning", 2: "heavy rain", 3: "heavy snow",
    4: "thunderstorm/lightning", 5: "hailstorm", 6: "dust storm",
    7: "dust raising winds", 8: "strong surface winds", 9: "heat wave",
    10: "hot day", 11: "warm night", 12: "cold wave", 13: "cold day",
    14: "ground frost", 15: "fog", 16: "very heavy rain",
    17: "extremely heavy rain",
}

def enabled() -> bool:
    return os.getenv("IMD_API_ENABLED", "false").lower() == "true"

def _timestamp(row: dict) -> datetime:
    issued = str(row["Date"]).strip()
    time = str(row.get("UTC", "0000")).strip().replace(":", "").zfill(4)
    if not time.isdigit() or len(time) != 4:
        raise ValueError("Invalid IMD issue time")
    return datetime.strptime(issued + time, "%Y-%m-%d%H%M").replace(tzinfo=timezone.utc)

def parse_warning(row: dict, *, now: datetime | None = None) -> dict:
    if not isinstance(row, dict):
        raise ValueError("Invalid official provider record")
    now = now or datetime.now(timezone.utc)
    issued = _timestamp(row)
    age = (now - issued).total_seconds() / 3600
    if age < -2 or age > ISSUE_MAX_AGE_HOURS:
        raise ValueError("IMD district bulletin is stale or future-dated")
    district = str(row.get("District", "")).strip()
    district_id = str(row.get("Obj_id", row.get("OBJ_ID", ""))).strip()
    if not district or len(district) > 150 or not district_id.isdigit():
        raise ValueError("District identity missing or malformed")
    days = []
    for n in range(1, 6):
        # Official schema is Day_1 ... Day_5, and Day1_Color ... Day5_Color.
        code_str = str(row.get(f"Day_{n}", "")).strip()
        raw_color = str(row.get(f"Day{n}_Color", "")).strip()
        if not code_str or not raw_color:
            raise ValueError("Missing daily warning code or level")
        try:
            parsed_codes = [int(value.strip()) for value in code_str.split(",")]
            level = int(raw_color)
        except ValueError as exc:
            raise ValueError("Unrecognized IMD warning codes") from exc
        if level not in COLOR or not all(c in CODES for c in parsed_codes):
            raise ValueError("Unrecognized official warning code/color")
        days.append({
            "day": n, "codes": parsed_codes, "phenomena": [CODES[c] for c in parsed_codes],
            "color": COLOR[level], "color_code": level,
        })
    return {
        "district": district, "district_id": district_id,
        "issued_at_utc": issued.isoformat(), "age_hours": round(age, 2),
        "days": days, "source_type": "imd_direct_api_response",
        "provider": "India Meteorological Department",
        "original_source_url": f"{DISTRICT_WARNINGS}?id={district_id}",
        "documentation_url": DOCUMENTATION_URL,
        "freshness_verified": True,
        "official_api_response": True,
        "republished_without_authority_endorsement": True,
        "note": "Check the original IMD bulletin. This application is not an official emergency channel.",
    }

def normalize_response(payload, district_id: int) -> dict:
    # IMD gateway responses may be raw records or nested; never guess safety on unsupported data.
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = next((v for k, v in payload.items() if k in ("data", "Data", "records") and isinstance(v, list)), [payload])
    else:
        raise ValueError("Unsupported IMD payload")
    for row in records:
        if not isinstance(row, dict):
            continue
        if str(row.get("Obj_id", row.get("OBJ_ID", ""))).strip() == str(district_id):
            return parse_warning(row)
    raise ValueError("Official district not found in response")

async def fetch_district_warning(district_id: int) -> dict:
    if not enabled():
        raise RuntimeError("IMD official API integration not enabled")
    if district_id < 1 or district_id > 999999:
        raise ValueError("Invalid district identifier")
    headers = {"Accept": "application/json", "User-Agent": "CivicShieldAI-Research/0.2"}
    token = os.getenv("IMD_API_BEARER_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient(timeout=httpx.Timeout(8), follow_redirects=False) as client:
        response = await client.get(DISTRICT_WARNINGS, params={"id": district_id}, headers=headers)
        response.raise_for_status()
        if len(response.content) > 2_000_000:
            raise ValueError("IMD response too large")
        return normalize_response(response.json(), district_id)
