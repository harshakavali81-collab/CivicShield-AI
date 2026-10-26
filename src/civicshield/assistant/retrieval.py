"""Source-linked *curated* mini knowledge corpus with offline lexical search.

This is retrieval, not generative AI, live ingestion or an official alert feed.
Source URLs link to original organizations but content is manually authored summaries.
"""
from __future__ import annotations
import re
from datetime import date

DOCUMENTS = [
    {
        "id": "flood-basics", "topic": "flood", "title": "Flood preparedness (educational summary)",
        "body": "Avoid walking or driving through floodwater. Check local warnings and move away from moving water. Keep drinking water, medicine and contact information available.",
        "keywords": "flood rain inundation monsoon waterlogging river varada వరద बारिश बाढ़ வெள்ளம் ಪ್ರವಾಹ",
        "source_title": "India National Disaster Management Authority",
        "source_url": "https://ndma.gov.in/",
        "curated_date": "2026-10-26", "translation_verified": False,
    },
    {
        "id": "heat-basics", "topic": "heat", "title": "Heat safety (educational summary)",
        "body": "Drink water regularly, avoid exertion in extreme heat, seek shade, and seek urgent medical advice for confusion or collapse.",
        "keywords": "heatwave hot heatstroke sun temperature వేడి गर्मी வெப்ப ಬಿಸಿ",
        "source_title": "India National Disaster Management Authority",
        "source_url": "https://ndma.gov.in/",
        "curated_date": "2026-10-26", "translation_verified": False,
    },
    {
        "id": "weather-forecasts", "topic": "forecast", "title": "Where to check meteorological notices",
        "body": "Consult the original India Meteorological Department website for current forecasts and official bulletins. This project does not ingest or validate IMD alerts.",
        "keywords": "weather forecast rainfall meteorology imd notice alert warning मौसम వాతావరణ வானிலை ಹವಾಮಾನ",
        "source_title": "India Meteorological Department",
        "source_url": "https://mausam.imd.gov.in/",
        "curated_date": "2026-10-26", "translation_verified": False,
    },
    {
        "id": "river-level", "topic": "water", "title": "River and flood information references",
        "body": "Check Central Water Commission channels and local authorities for authentic river-level and flood communications. This platform has no live river data.",
        "keywords": "river level flood river gauge dam reservoir water cwc नदी వరద ஆறு ನದಿ",
        "source_title": "Central Water Commission",
        "source_url": "https://cwc.gov.in/",
        "curated_date": "2026-10-26", "translation_verified": False,
    },
    {
        "id": "preparedness", "topic": "general", "title": "Family preparedness checklist",
        "body": "Keep important contacts, water, medicines, and portable light accessible. Plan communication with family members and follow local emergency authority instructions.",
        "keywords": "emergency kit prepare medicine emergency bag evacuation shelter आपातकाल అత్యవసర அவசர ತುರ್ತು",
        "source_title": "India National Disaster Management Authority",
        "source_url": "https://ndma.gov.in/",
        "curated_date": "2026-10-26", "translation_verified": False,
    },
]

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[\w\u0900-\u097f\u0c00-\u0c7f\u0b80-\u0bff\u0c80-\u0cff]{2,}", text.casefold(), flags=re.UNICODE))

def search_docs(query: str, limit: int = 3) -> list[dict]:
    words = tokenize(query)
    if not words:
        return []
    scored = []
    for document in DOCUMENTS:
        tokens = tokenize(" ".join((
            document["title"], document["body"], document["keywords"], document["topic"]
        )))
        hits = len(words & tokens)
        if hits:
            scored.append((hits, document["id"], document))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [{key: value for key, value in document.items() if key != "keywords"} for _, _, document in scored[:limit]]
