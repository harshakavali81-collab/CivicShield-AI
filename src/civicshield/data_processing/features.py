"""Shared feature definition prevents offline/online feature mismatch."""
FEATURE_COLUMNS = ["rainfall_24h_mm", "temperature_c", "humidity_pct"]

def feature_record(rainfall_24h_mm: float, temperature_c: float, humidity_pct: float) -> dict:
    return {
        "rainfall_24h_mm": float(rainfall_24h_mm),
        "temperature_c": float(temperature_c),
        "humidity_pct": float(humidity_pct),
    }
