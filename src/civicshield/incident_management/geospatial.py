"""Distance calculation for restricted LOCAL reviewer search; not an emergency routing tool."""
import math

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    a, b, c, d = map(math.radians, (lat1, lon1, lat2, lon2))
    delta_lat, delta_lon = c - a, d - b
    v = math.sin(delta_lat / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin(delta_lon / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(v), math.sqrt(max(0, 1 - v)))
