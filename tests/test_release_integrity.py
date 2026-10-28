"""Guard v0.2.0 portfolio release consistency and visible safety notices."""
from pathlib import Path
import tomllib
from backend.app.main import app

ROOT = Path(__file__).resolve().parents[1]

def test_project_metadata_and_running_api_versions_agree():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))
    assert app.version == metadata["project"]["version"] == "0.2.0"

def test_portfolio_docs_and_licensing_are_present():
    files = ("README.md", "LICENSE", "SECURITY.md", "CHANGELOG.md",
        "CONTRIBUTING.md", "docs/CASE_STUDY.md",
        "docs/RELEASE_CHECKLIST.md", "docs/ROADMAP.md")
    assert all((ROOT / name).is_file() for name in files)

def test_documentation_has_explicit_scope_warning():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    case_study = (ROOT / "docs/CASE_STUDY.md").read_text(encoding="utf-8").lower()
    assert "not an official warning" in readme
    assert "fabricated" in case_study
    assert "no emergency advice" in case_study
    assert "scenario lab" in readme
