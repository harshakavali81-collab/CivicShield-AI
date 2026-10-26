"""Keyword-based *suggestions* only; authorized humans make all final decisions."""
import hashlib
import re

KEYWORDS = {
    "flooding": ("flood", "waterlogging", "flooded", "వరద", "बाढ़", "வெள்ளம்", "ಪ್ರವಾಹ"),
    "fallen_tree": ("tree", "fallen branch", "చెట్టు", "पेड़", "மரம்", "ಮರ"),
    "road_block": ("blocked", "roadblock", "closed road", "రోడ్డు", "सड़क", "சாலை", "ರಸ್ತೆ"),
    "heat": ("heatstroke", "extreme heat", "వేడి", "गर्मी", "வெப்ப", "ಬಿಸಿ"),
}
URGENT_TERMS = ("trapped", "injured", "stranded", "hospital", "help urgently")

def redact_contact_info(value: str) -> str:
    value = re.sub(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", "[email redacted]", value)
    value = re.sub(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", "[phone redacted]", value)
    return value

def categorize(title: str, description: str) -> str:
    body = (title + " " + description).lower()
    for category, needles in KEYWORDS.items():
        if any(word in body for word in needles):
            return category
    return "other"

def priority_hint(title: str, description: str, category: str) -> str:
    body = (title + " " + description).lower()
    if any(w in body for w in URGENT_TERMS):
        return "review_soon"
    return "normal"

def duplicate_fingerprint(title: str, city: str, category: str) -> str:
    # Advisory exact-match heuristic only. Never automatically suppress reports.
    normalized = re.sub(r"\W+", " ", title.lower()).strip()
    payload = "|".join((normalized, city.lower().strip(), category))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
