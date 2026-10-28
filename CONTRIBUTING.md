# Contributing to CivicShield AI

Contributions are welcome for **educational and non-operational** software improvements. This repository cannot accept incident details involving real persons, private geolocation traces, non-licensed model training data, credentials, or unreviewed official emergency messages.

## Local developer setup

```bash
git clone https://github.com/harshakavali81-collab/CivicShield-AI.git
cd CivicShield-AI
python -m venv .venv
python -m pip install -e ".[dev,migrations]"
pytest -q
python -m scripts.doctor --mode local
```

Frontend: `cd frontend && npm install && npm run build`. For API integration: start `uvicorn backend.app.main:app --reload`, then `python -m scripts.smoke_demo`.

## Pull request quality requirements

1. Explain whether each new data element is *synthetic*, *manually curated*, *user-submitted and unverified*, *third-party modeled*, or *verifiable official source*.
2. Add tests for new branches, bounds, failures and stale/missing source states. Never substitute invented emergency or prediction scores for evaluation evidence.
3. Maintain fail-closed identity and government-source behavior. Do not turn provider failures into “safe” or “no warning.”
4. Protect personal data and never commit real report narratives, location trails, database exports or cloud secrets.
5. Update API docs, the technical case study, roadmap and demo script for user-facing behavior.
6. Keep all portfolio artwork clearly labeled as conceptual when it is not a real UI capture.
7. Review third-party image, geographic tile, data and dependency licenses.

## Engineering boundaries

Unverified user reports must never be silently presented as government-confirmed events, and no AI score may automatically trigger rescue, evacuation or emergency notifications.

See [security](SECURITY.md), [test plan](docs/TEST_PLAN.md), [case study](docs/CASE_STUDY.md), and [roadmap](docs/ROADMAP.md).
