# Architecture and trust boundaries

> **Scope:** research/portfolio demonstration. No live emergency alert feed or government integration.

## Component architecture

~~~mermaid
flowchart TB
  U[Public React client] --> P[FastAPI public endpoints]
  R[Local authorized reviewer] -->|X-Responder-Key demo auth| Q[Restricted incident review routes]
  P --> V[Pydantic validation]
  V --> F[Six-hour freshness gate]
  F --> M{Trusted local model configured?}
  M -->|No| H[Illustrative rainfall heuristic]
  M -->|Yes| E[Optional user-trained sklearn model]
  H --> O[Experimental indicator, never warning]
  E --> O
  P --> S[Curated multilingual preparedness guidance]
  P --> I[Sanitized incident submission]
  I --> D[(SQLite local / PostgreSQL Docker)]
  Q --> D
  D --> A[Aggregate local-report counts]
  O --> U
  S --> U
  A --> U
  G[IMD / NDMA / CWC websites] -. user follows link .-> U
~~~

## Deployment graph

~~~mermaid
flowchart LR
  Browser -->|localhost:5173| N[nginx + React]
  N -->|/api| API[FastAPI :8000]
  API --> DB[(PostgreSQL + PostGIS extension)]
  API --> Train[Optional locally trusted joblib artifact]
  CI[GitHub Actions] --> Tests[pytest + Vite build]
~~~

## Processing contracts

1. **Weather example / user observations** — no automated external feed is loaded; \`source_type\` states origin.
2. **Validation** — Pydantic bounds; stale inputs older than 6 h return unavailable, not safe.
3. **Experimental scoring** — deterministic rainfall heuristic or opted-in classifier; never represents official flood warning. No geographic safety inference.
4. **Incident intake** — redacts basic phone/email patterns, classifies keywords, suggests priority, tracks duplicates without suppression, persists only when operator enables it.
5. **Human decisions** — a configured shared key is required to review/verify. Demo verification means a local reviewer changed a status, not official verification.
6. **Multilingual retrieval** — current version uses embedded curated summaries and linked official homepages, *not* real-time multilingual RAG.

## What is not implemented

No genuine IMD API authentication/data ingestion; no calibrated flood forecasting; no SHAP; no LLM retrieval or vector store; no public geospatial overlays; no multi-tenant OIDC; no notification/dispatch; no real MLOps drift dashboard. Follow [ROADMAP](ROADMAP.md).
