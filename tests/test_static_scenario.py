"""Static and API case studies must be the same fabricated dataset."""
from scripts.export_static_demo import OUTPUT, canonical_scenario, parse_export, render, verify
from scripts.verify_site import validate_site

def test_static_dataset_equals_api_source_and_is_offline():
    verify()
    exported = parse_export(OUTPUT.read_text(encoding="utf-8"))
    assert exported == canonical_scenario()
    assert exported["source_type"] == "synthetic_portfolio_exercise"
    assert exported["official_data_connected"] is False
    assert exported["external_services_called"] is False
    assert exported["database_reports_created"] == 0
    assert len(exported["samples"]) == 24

def test_export_generator_is_deterministic():
    assert render() == render()
    assert parse_export(render()) == canonical_scenario()

def test_portfolio_links_to_offline_demo_and_scripts_are_local():
    result = validate_site()
    assert result["result"] == "static_portfolio_verified"
    assert result["offline_demo"] is True
    assert result["offline_data_matches_api"] is True
