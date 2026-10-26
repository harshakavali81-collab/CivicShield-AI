# Model card — CivicShield AI experimental risk indicator

## Intended scope

Education and ML system design portfolio **only**. NOT emergency, medical, insurance, evacuation or public warning decisions.

## Two modes

1. **Default demonstration heuristic:** manually entered 24-hour rainfall grouped into illustrative labels. Below 30mm lower indicator; 30–64.999 elevated; 65–114.999 high; at least 115 very high. These are *not validated flood thresholds* and must not be described as official warning criteria. Temperature and humidity are ignored in this mode.
2. **Optional local trained classifier:** a RandomForestClassifier using rainfall, temperature, humidity on user-owned historical labeled data. No pretrained/validated weights are distributed; artifacts must be generated locally and should never be loaded from untrusted people.

## Data

No external observations shipped. The train command requires at least 50 binary-labeled, timestamped examples and both classes on either side of a chronological 80/20 holdout. A 50-row train check is a code guard, **not** a scientifically adequate recommended dataset size.

## Evaluation

The experiment exports balanced accuracy, a precision/recall/F1 report and confusion matrix. The holdout is chronological but **not** spatially independent. User must evaluate geographic shifts, temporal leakage, false negatives, subgroup variation, calibration, imbalanced alerts, missing data, and real downstream harms before real-world testing.

## Threshold flowchart

~~~mermaid
flowchart TD
  A[Input age > 6h?] -->|Yes| U[Unavailable]
  A -->|No| B{Rainfall mm in 24h}
  B -->|< 30| C[Lower indicator; never means safe]
  B -->|30 to < 65| D[Elevated demo indicator]
  B -->|65 to < 115| E[High demo indicator]
  B -->|>=115| F[Very high demo indicator]
~~~

## Fairness, uncertainty and limitations

This does not model terrain, storm surge, drainage, infrastructure, observed inundation, response capacity, sensor bias or time-of-day. No predictive confidence interval, calibrated probability, explainability (SHAP), uncertainty bounds, model drift or independent real-world validity is claimed.

**Safety invariant:** stale data => unavailable; missing official feed => unknown; low score never => safe.

## Future validation gates

Source contracts; legal data provenance; expert-labeled events; out-of-region test sets; holdout and lead-time definition; false-negative analysis; calibration; stress tests; sign-off from relevant domain experts; monitoring and rollback.
