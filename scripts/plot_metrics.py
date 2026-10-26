"""Generate portable SVG evaluation graphs from YOUR model metrics JSON.

Run: python scripts/plot_metrics.py artifacts/models/risk_model.metrics.json
These are experiment summaries, never validated public-safety performance claims.
"""
from __future__ import annotations
import argparse
import json
from html import escape
from pathlib import Path

SVG_START = '<svg xmlns="http://www.w3.org/2000/svg" width="750" height="410" viewBox="0 0 750 410" role="img">'
SVG_END = "</svg>"

def confusion_svg(matrix: list[list[int]]) -> str:
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("Expected a 2x2 confusion matrix")
    cells = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            value = int(value)
            if value < 0:
                raise ValueError("Counts must be nonnegative")
            x, y = 190 + j * 170, 105 + i * 120
            bg = "#e6f1ff" if i == j else "#fff0e7"
            cells.append(
                f'<rect x="{x}" y="{y}" width="155" height="105" rx="10" fill="{bg}"/>'
                f'<text x="{x+77}" y="{y+60}" font-size="30" fill="#1c3e60" '
                f'text-anchor="middle" font-weight="bold">{value}</text>'
            )
    return (
        SVG_START
        + '<rect width="750" height="410" fill="#ffffff"/>'
        + '<text x="32" y="41" font-family="Arial" font-weight="bold" font-size="22" fill="#172945">Confusion matrix</text>'
        + '<text x="32" y="63" font-family="Arial" font-size="13" fill="#52657c">Experimental holdout only — not a safety validation</text>'
        + '<text x="272" y="94" font-family="Arial" font-size="14" fill="#44566f">Predicted 0</text>'
        + '<text x="443" y="94" font-family="Arial" font-size="14" fill="#44566f">Predicted 1</text>'
        + '<text x="93" y="160" font-family="Arial" font-size="14" fill="#44566f">Actual 0</text>'
        + '<text x="93" y="282" font-family="Arial" font-size="14" fill="#44566f">Actual 1</text>'
        + "".join(cells)
        + '<text x="32" y="381" font-family="Arial" font-size="12" fill="#777">Generated from local user-supplied data; never an official warning score</text>'
        + SVG_END
    )

def classification_svg(report: dict) -> str:
    bars = []
    entries = [(label, key, color) for label in ("0", "1") for key, color in (
        ("precision", "#407ee6"), ("recall", "#36a6a0")
    )]
    for index, (label, key, color) in enumerate(entries):
        value = float(report.get(label, {}).get(key, 0))
        if not 0 <= value <= 1:
            raise ValueError("Classification metric out of range")
        y = 112 + index * 59
        width = round(value * 430, 2)
        bars.extend([
            f'<text x="42" y="{y+16}" font-family="Arial" font-size="14" fill="#354b69">Class {escape(label)} · {escape(key)}</text>',
            f'<rect x="215" y="{y}" width="430" height="22" rx="6" fill="#e9eff8"/>',
            f'<rect x="215" y="{y}" width="{width}" height="22" rx="6" fill="{color}"/>',
            f'<text x="660" y="{y+17}" font-family="Arial" font-size="13" fill="#233956">{value:.2f}</text>',
        ])
    return (
        SVG_START
        + '<rect width="750" height="410" fill="#ffffff"/>'
        + '<text x="32" y="41" font-family="Arial" font-weight="bold" font-size="22" fill="#172945">Precision and recall by class</text>'
        + '<text x="32" y="63" font-family="Arial" font-size="13" fill="#52657c">Experimental holdout only — no generalization claim</text>'
        + "".join(bars)
        + '<text x="32" y="381" font-family="Arial" font-size="12" fill="#777">Investigate false negatives, regions, lead time and class prevalence</text>'
        + SVG_END
    )

def render_report(metrics_path: str | Path, output_dir: str | Path) -> list[Path]:
    metrics = json.loads(Path(metrics_path).read_text(encoding="utf-8"))
    matrix = metrics["confusion_matrix"]
    report = metrics["classification_report"]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    paths = [output / "confusion_matrix.svg", output / "classification_metrics.svg"]
    paths[0].write_text(confusion_svg(matrix), encoding="utf-8")
    paths[1].write_text(classification_svg(report), encoding="utf-8")
    return paths

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics_json")
    parser.add_argument("--output-dir", default="artifacts/evaluation_reports")
    args = parser.parse_args()
    for path in render_report(args.metrics_json, args.output_dir):
        print(path)

if __name__ == "__main__":
    main()
