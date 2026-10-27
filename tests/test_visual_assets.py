"""Check all committed SVG visual assets and GitHub/site references."""
from pathlib import Path
import re
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = "{http://www.w3.org/2000/svg}"
VISUALS = ROOT / "docs" / "assets"
SITE = ROOT / "site"

def parse_svg(file_path: Path) -> ET.Element:
    root = ET.parse(file_path).getroot()
    assert root.tag == NAMESPACE + "svg", file_path
    assert root.get("viewBox"), file_path
    assert root.get("width") and root.get("height"), file_path
    assert root.find(NAMESPACE + "title") is not None, file_path
    assert any((node.text or "").strip() for node in root.findall(".//" + NAMESPACE + "text")), file_path
    for node in root.iter():
        assert node.tag != NAMESPACE + "script", file_path
        assert not any(name.lower().startswith("on") for name in node.attrib), file_path
        for key, value in node.attrib.items():
            if key.endswith("href") or key == "href":
                assert not value.lower().startswith(("http:", "https:", "javascript:", "data:")), file_path
    return root

def test_original_visual_gallery_is_accessible_and_valid():
    files = list(VISUALS.glob("*.svg"))
    assert len(files) >= 8
    for svg_path in files:
        parse_svg(svg_path)

def test_self_contained_portfolio_visuals_exist_and_parse():
    files = list((SITE / "assets").glob("*.svg"))
    assert len(files) >= 3
    for svg_path in files:
        parse_svg(svg_path)
    source = (SITE / "index.html").read_text(encoding="utf-8")
    for relative in re.findall(r'src="(assets/[^"]+\.svg)"', source):
        assert (SITE / relative).exists(), relative
    assert "No live" in source or "NO live" in source

def test_all_readme_diagrams_resolve_locally():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    paths = set(re.findall(r'docs/assets/[\w.-]+\.svg', text))
    assert len(paths) >= 7
    for item in paths:
        assert (ROOT / item).is_file(), item

def test_gallery_docs_reference_existing_images():
    for name in ("VISUALIZATIONS.md", "ARCHITECTURE.md", "PROJECT_WORKFLOW.md", "MODEL_CARD.md"):
        file_path = ROOT / "docs" / name
        md = file_path.read_text(encoding="utf-8")
        for rel in re.findall(r'\((assets/[^)]+\.svg)\)', md):
            assert (file_path.parent / rel).is_file(), (name, rel)

def test_design_is_explicitly_not_an_official_alert():
    markdown = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    for phrase in ("concept", "not an official warning", "not screenshots"):
        assert phrase in markdown
