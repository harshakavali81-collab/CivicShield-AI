# 3-minute interview walkthrough

## 0:00–0:35 — Context

"CivicShield AI is a full-stack public-safety research demonstration. It combines a FastAPI backend, a React dashboard, supervised ML training experiments and a human incident-review workflow. I designed safety boundaries so experimental results can never be confused with government warnings."

## 0:35–1:10 — Architecture

Open [ARCHITECTURE](ARCHITECTURE.md). Explain source provenance, data validation, six-hour freshness gate, SQL persistence and React visualizations.

## 1:10–1:45 — Risk explorer

Use default sample inputs (clearly synthetic) and show "high" **illustrative** grouping, an explanation, and \`is_official_warning=false\`. Change input age to seven hours and demonstrate that the system refuses to label risk.

## 1:45–2:20 — Multilingual + incidents

Ask about flooding in Telugu, Hindi or English; show curated answers and linked authority. Explain that reports undergo deduplication and that only a human can change their review status. Reporting disabled by default unless an operator opts in.

## 2:20–3:00 — Engineering and limitations

Point to training script, temporal holdout tests, Docker and CI. Explicitly distinguish ML demo from operational forecasting. Name the next milestone: curated datasets and independent validation.

## Resume bullets (accurate to repository)

- Developed a modular FastAPI/React demonstration platform with multilingual preparedness guidance, interactive map, SQL-backed incident review and analytics visualizations.
- Implemented an optional Scikit-learn risk-classification experiment with chronological evaluation and safety guards for stale weather inputs.
- Added automated API/model tests, Docker Compose and CI while documenting data provenance, security risks and limitations.
