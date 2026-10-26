"""Simple bounded population shift heuristic, not a substitute for continuous MLOps."""
from __future__ import annotations
import math
from statistics import mean, pstdev

def distribution_shift(reference: list[float], current: list[float]) -> dict:
    if len(reference) < 20 or len(current) < 20:
        return {"status": "insufficient_data", "drift_score": None}
    if not all(math.isfinite(float(x)) for x in reference + current):
        raise ValueError("Inputs must be finite")
    baseline = mean(reference)
    spread = pstdev(reference)
    if spread == 0:
        return {"status": "constant_reference", "drift_score": None}
    z = abs(mean(current) - baseline) / spread
    return {
        "status": "review_recommended" if z > 1 else "no_mean_shift_detected",
        "drift_score": round(z, 3),
        "metric": "absolute_mean_shift_in_reference_stddevs",
        "note": "Only a mean-shift heuristic. Not a validated drift detector or operating alert.",
    }
