# Four-minute software/AI engineering interview walkthrough

## 0:00–0:35 — Problem and scope

"CivicShield AI is a research demonstration for disaster-related situational awareness. It combines data provenance, reproducible ML experiments, a multilingual educational interface and a human incident-review workflow. I explicitly avoid confusing it with a government warning platform."

## 0:35–1:15 — Application architecture

Show [Architecture](ARCHITECTURE.md). Explain FastAPI, SQLAlchemy, React charts, Leaflet, the six-hour freshness gate and the optional Postgres/PostGIS setup. Point to GitHub Actions.

## 1:15–1:50 — Live third-party modeled weather vs experimental risk

Use the weather explorer to show Open-Meteo timestamp, attribution and modeled values (if opted in and provider available). Then switch to the **separate** risk demo to show a sample input. Explain why a model output cannot establish whether a road is safe. Change age to seven hours and show \`unavailable\`.

## 1:50–2:30 — Multilingual guidance and source search

Ask about floods in Telugu/English/Hindi. Search the small curated source library and show original-authority bookmarks. Stress this is currently manual summary retrieval, not a live government corpus or generative RAG agent.

## 2:30–3:20 — Human reports and access control

Demonstrate a sample local submission using opt-in intake; report classification, duplicate flags, reviewer-only queue, geographic search and audit history. Show that no alerts or dispatch happen automatically.

## 3:20–4:00 — ML reproducibility, graphs and production gaps

Explain chronological holdout, confusion matrix, SHAP/MLflow optional helpers, migration tests, local backup and privacy purge. Close by naming external-validation, OIDC security and official-feed licensing as real production blockers.

## Accurate resume bullets

- Built a modular React/FastAPI public-safety *research demonstration* with source-attributed third-party modeled weather, map visualizations, multilingual educational guidance, SQL-backed incident review and restricted geographic queries.
- Implemented reproducible Scikit-learn experimental training/evaluation, data quality checks, freshness guards, optional explainability, and source-provenance documentation.
- Added CI tests, a PostgreSQL-capable data layer, Alembic initial migration, local backups, reviewer audit history and safety/security guardrails.

**Interview integrity:** Do not claim production deployment, officially verified safety predictions, third-party partnerships or validated emergency benefits.
