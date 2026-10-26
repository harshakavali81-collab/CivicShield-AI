"""Freshness gate: unknown or outdated observations cannot generate a risk indicator."""
MAX_AGE_HOURS = 6.0

def is_fresh(age_hours: float) -> bool:
    return 0 <= age_hours <= MAX_AGE_HOURS
