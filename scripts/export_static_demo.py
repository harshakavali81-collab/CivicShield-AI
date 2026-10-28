"""Export the canonical fictional case study for offline browsers (no packages needed).

The checked-in site/scenario-data.js and backend API must carry equivalent
synthetic data. Use --check in CI, or run without flags to regenerate the file.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site" / "scenario-data.js"
PREFIX = "window.CIVICSHIELD_SCENARIO = "

def canonical_scenario() -> dict:
    source = ROOT / "src" / "civicshield" / "demo" / "scenarios.py"
    return runpy.run_path(str(source))["build_scenario"]()

def parse_export(content: str) -> dict:
    if not content.startswith(PREFIX) or not content.endswith(";\n"):
        raise ValueError("Scenario export must be a single data assignment")
    parsed = json.loads(content[len(PREFIX):-2])
    if not isinstance(parsed, dict):
        raise ValueError("Scenario payload must be a JSON object")
    return parsed

def render() -> str:
    return PREFIX + json.dumps(canonical_scenario(), ensure_ascii=False,
                               separators=(",", ":")) + ";\n"

def verify() -> None:
    if parse_export(OUTPUT.read_text(encoding="utf-8")) != canonical_scenario():
        raise ValueError("Static offline case study has drifted from Python canonical data")
    scenario = canonical_scenario()
    if not (scenario["is_synthetic"] and scenario["external_services_called"] is False
            and scenario["is_official_warning"] is False
            and scenario["database_reports_created"] == 0):
        raise ValueError("Static demo must remain clearly fictional")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify checked-in export, without changes")
    args = parser.parse_args()
    try:
        if args.check:
            verify()
            print("Canonical offline scenario matches backend data and requires no network.")
        else:
            OUTPUT.write_text(render(), encoding="utf-8")
            verify()
            print(f"Wrote {OUTPUT.relative_to(ROOT)}; synthetic dataset verified.")
    except (ValueError, OSError) as error:
        print(f"Offline scenario verification failed: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
