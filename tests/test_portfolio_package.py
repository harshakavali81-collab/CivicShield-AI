"""Ensure portfolio archive is reproducible and contains no source secrets."""
import hashlib
import json
from pathlib import Path
import zipfile
from scripts.package_portfolio import package_site, NAME

def test_offline_portfolio_is_deterministic_and_source_only(tmp_path):
    first, second = tmp_path / "one", tmp_path / "two"
    a = package_site(first)
    b = package_site(second)
    assert a["status"] == b["status"] == "static_portfolio_packaged"
    content = (first / NAME).read_bytes()
    assert content == (second / NAME).read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    assert (first / (NAME + ".sha256")).read_text().startswith(digest)
    with zipfile.ZipFile(first / NAME) as archive:
        names = archive.namelist()
        assert {"index.html", "favicon.svg", "MANIFEST.json", "robots.txt"} <= set(names)
        assert any(n.startswith("assets/") and n.endswith(".svg") for n in names)
        assert not any(n.startswith((".env", "backend/", "data/", ".git/", "backups/")) for n in names)
        manifest = json.loads(archive.read("MANIFEST.json"))
        assert manifest["not_an_emergency_service"] is True
        assert manifest["contains_real_incident_data"] is False
        for entry in manifest["files"]:
            assert hashlib.sha256(archive.read(entry["path"])).hexdigest() == entry["sha256"]

def test_zip_does_not_follow_symlinks(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("Research only")
    (tmp_path / "private.txt").write_text("secret")
    link = site / "out.txt"
    try:
        link.symlink_to(tmp_path / "private.txt")
    except (OSError, NotImplementedError):
        return
    from pytest import raises
    with raises(ValueError, match="Symbolic links"):
        package_site(tmp_path / "out", site)
