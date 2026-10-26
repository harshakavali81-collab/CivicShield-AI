"""The chart generator must produce readable SVGs from evaluation output."""
import json
from scripts.plot_metrics import render_report, confusion_svg

def test_render_report(tmp_path):
    metrics = tmp_path / "metrics.json"
    metrics.write_text(json.dumps({
        "confusion_matrix": [[12, 2], [3, 10]],
        "classification_report": {
            "0": {"precision": 0.8, "recall": 0.9},
            "1": {"precision": 0.7, "recall": 0.8},
        },
    }), encoding="utf-8")
    paths = render_report(metrics, tmp_path / "plots")
    assert len(paths) == 2
    assert all(p.is_file() for p in paths)
    assert all("<svg" in p.read_text() for p in paths)
    assert "Precision and recall" in paths[1].read_text()

def test_confusion_rejects_invalid_matrix():
    try:
        confusion_svg([[1]])
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid confusion matrix must be rejected")
