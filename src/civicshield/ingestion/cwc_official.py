"""Official CWC forecast references. No undocumented API is assumed.

The official forecasts are available through CWC's documented websites.
Do not scrape a proprietary portal or invent a machine-readable alert feed.
"""
OFFICIAL_LINKS = [
    {"title": "CWC Flood Forecasting", "url": "https://ffs.india-water.gov.in/"},
    {"title": "CWC Seven-day Advisory Flood Forecast", "url": "https://aff.india-water.gov.in/"},
    {"title": "Central Water Commission", "url": "https://cwc.gov.in/"},
]

def integration_status() -> dict:
    return {
        "provider": "Central Water Commission",
        "mode": "authoritative_external_links_only",
        "api_connected": False,
        "official_alerts": None,
        "reason": "No authorized, documented API credentials and schema have been configured.",
        "references": OFFICIAL_LINKS,
        "warning": "No integration does not mean no CWC flood warnings exist.",
    }
