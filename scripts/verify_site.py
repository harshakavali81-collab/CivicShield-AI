"""Offline asset and safety-text audit for the static GitHub Pages portfolio."""
from __future__ import annotations
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.links = []
        self.scripts = []
        self.missing_alt = []
        self.ids = []
        self.skip_link = False

    def handle_starttag(self, tag, raw_attrs):
        attrs = dict(raw_attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "script":
            self.scripts.append(attrs.get("src", "inline"))
        if tag == "img":
            src = attrs.get("src", "")
            self.images.append(src)
            if not attrs.get("alt", "").strip():
                self.missing_alt.append(src)
        if tag in ("a", "link"):
            href = attrs.get("href", "")
            if href == "#main-content":
                self.skip_link = True
            if href and not href.startswith(("http://", "https://", "#", "mailto:", "tel:")):
                self.links.append(href)
            if href.startswith("http://"):
                raise ValueError("External hyperlinks must use HTTPS")

def static_asset(name: str) -> Path:
    parsed = urlparse(name)
    if parsed.scheme or parsed.netloc or name.startswith("/") or "\\" in name:
        raise ValueError(f"Invalid relative asset: {name}")
    parts = Path(parsed.path).parts
    if not parts or ".." in parts:
        raise ValueError(f"Unsafe relative asset: {name}")
    path = SITE / parsed.path
    if not path.is_file():
        raise FileNotFoundError(f"Missing asset: {name}")
    return path

def validate_site() -> dict:
    html = (SITE / "index.html").read_text("utf-8")
    parser = SiteParser()
    parser.feed(html)
    assert parser.skip_link and "main-content" in parser.ids
    assert len(parser.images) >= 5
    assert not parser.scripts, "Static portfolio should have no scripts or data fetches"
    assert not parser.missing_alt, f"Missing image alt: {parser.missing_alt}"
    for resource in parser.images + parser.links:
        asset = static_asset(resource)
        if asset.suffix == ".svg":
            svg = ET.parse(asset).getroot()
            assert svg.tag == "{http://www.w3.org/2000/svg}svg"
            assert svg.find("{http://www.w3.org/2000/svg}title") is not None
    assert (SITE / "robots.txt").is_file()
    assert "fictional" in html.lower()
    assert "not an emergency service" in html.lower()
    return {"result": "static_portfolio_verified", "images": len(parser.images),
            "local_assets_checked": len(parser.images) + len(parser.links),
            "public_emergency_service": False, "real_live_data": False}

if __name__ == "__main__":
    try:
        print(validate_site())
    except (AssertionError, ValueError, FileNotFoundError, ET.ParseError) as error:
        print(f"Static portfolio check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
