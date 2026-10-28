"""Contract for the self-contained, appropriately labeled GitHub Pages site."""
import pytest
from scripts.verify_site import SiteParser, static_asset, validate_site

def test_static_portfolio_has_all_local_images_and_accessibility():
    status = validate_site()
    assert status["result"] == "static_portfolio_verified"
    assert status["images"] >= 5
    assert status["public_emergency_service"] is False

@pytest.mark.parametrize("path", ["../.env", "/etc/passwd", "http://bad.example", "assets/../index.html"])
def test_asset_path_cannot_escape_site(path):
    with pytest.raises(ValueError):
        static_asset(path)

def test_html_audit_detects_scripts_and_missing_alternative_text():
    parser = SiteParser()
    parser.feed('<img src="broken.svg"><script>danger</script>')
    assert parser.scripts
    assert parser.missing_alt == ["broken.svg"]
