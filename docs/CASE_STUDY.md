# CivicShield AI case study: Fictional Monsoon Readiness Exercise

> **Every event and number in this page is fabricated.** This is a deterministic educational software exercise for GitHub portfolio demonstration. No source corresponds to a real disaster, meteorological measurement, official district alert, government service, patient, or rescue decision. **No emergency advice is issued.**

![Illustrative CivicShield concept dashboard](assets/dashboard-concept.svg)

## Problem

A portfolio-level public-safety software prototype must demonstrate architecture, safe data labeling, frontend/backend integration, provenance, and human review without pretending that unvalidated AI outputs are official predictions.

## Architecture of this exercise

\`\`\`mermaid
flowchart LR
    A[Fixed fictional hourly arrays] --> B[Pure deterministic Python generator]
    B --> C[Read-only FastAPI endpoint]
    C --> D[React Scenario Lab]
    D --> E[Two-axis interactive illustrative chart]
    D --> F[Four selectable technical walkthrough stages]
    C --> G[Contract and safety tests]
    H[Live government feeds] -. NOT USED .-> B
    I[Incident database] -. NO WRITES .-> B
\`\`\`

## Implementation

- **Source**: \`src/civicshield/demo/scenarios.py\` (fixed, deterministic 24-hour arrays).
- **API endpoint**: \`GET /api/v1/demo/scenario\`, no external calls or database writes.
- **Frontend**: \`frontend/src/ScenarioLab.jsx\` with React state and Recharts.
- **API safety metadata**: \`source_type=synthetic_portfolio_exercise\`, \`is_synthetic=true\`, \`is_official_warning=false\`, \`official_data_connected=false\`, \`real_hazard_predictions=false\`.
- **Tests**: \`tests/test_scenario_lab.py\` verifies reproducibility, labels, sample integrity, no audit/incident writes, and no official-advisory claims.

## Four reproducible software stages

1. **Data provenance**: Distinguish synthetic sample values from sources with legal permissions, reliable timestamps and documented schemas. A disconnected IMD/CWC adapter never means there is no warning.
2. **Freshness validation**: A source age older than six hours is rejected by the independent experimental risk endpoint, which never returns an "all-clear" safety guarantee.
3. **Human report moderation**: A category and priority hint do not mean a report is confirmed. The fictional chart's report counts are deliberately **not** written to the incident database.
4. **Experimental model evaluation**: Spatial and temporal holdout code can be run against a *separately supplied authorized labeled dataset*. The fictional charts are not prediction scores, and no operational accuracy is claimed.

## Example commands

\`\`\`bash
python -c "from civicshield.demo.scenarios import build_scenario; s=build_scenario(); print(s['summary'])"
uvicorn backend.app.main:app --reload
python -m scripts.smoke_demo --url http://localhost:8000
pytest -q tests/test_scenario_lab.py
\`\`\`

Launch the frontend using \`cd frontend && npm install && npm run dev\`, then choose **Scenario lab**.

## Engineering talking points for interviews

- Reproducible, side-effect-free Python data generation with explicit metadata.
- REST contract and React frontend consumption with an empty/loading/error state.
- Recharts interactive visualization with distinct units and axes.
- Four stateful, accessible user-selected engineering stages.
- Contract regression tests that reject fabricated source identity or implied safety benefits.
- Honest documentation of **unmet** official data integration, identity provider, model validation and cloud deployment requirements.

## What this project does not prove

No claim of real-world flood prediction performance, evacuation guidance, validated risk classifications, field deployment, government data partnership or operational disaster response follows from this exercise. It demonstrates an engineering workflow, not public safety effectiveness.
