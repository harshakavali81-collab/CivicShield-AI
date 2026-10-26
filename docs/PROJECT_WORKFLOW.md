# End-to-end project workflow

## A. Risk indicator workflow

~~~mermaid
flowchart TD
  A[Manual weather input] --> B{Schema valid?}
  B -- No --> R[HTTP 422]
  B -- Yes --> C{Input age <= 6h?}
  C -- No --> U[Unavailable; never imply safety]
  C -- Yes --> D{Optional trusted model configured?}
  D -- Yes --> E[Experimental binary score, not calibrated]
  D -- No --> F[Illustrative rainfall thresholds]
  E --> G[Response with limitation and provenance]
  F --> G
  G --> H[Dashboard with demo warning]
~~~

## B. Citizen incident workflow

~~~mermaid
flowchart TD
  A[Report submitted] --> B{Opt-in submissions enabled?}
  B -- No --> X[HTTP 503: Disabled by default]
  B -- Yes --> C[Validate payload and redact basic contact patterns]
  C --> D[Keyword category + suggested priority]
  D --> E[Exact-title/city/category duplicate fingerprint]
  E --> F[(Store report; never auto-drop duplicates)]
  F --> G[Authenticated human review]
  G --> H{Reviewer decision}
  H --> I[Verified in demo]
  H --> J[Dismissed]
  H --> K[Needs information]
~~~

## C. Optional training workflow

~~~mermaid
flowchart LR
  D[User-owned labeled CSV] --> V[Schema / sample / class checks]
  V --> T[Chronological 80/20 split]
  T --> M[Random forest classifier]
  M --> E[Balanced accuracy, precision/recall, confusion matrix]
  E --> A[Local joblib + JSON metrics]
  A --> S[Opt-in backend runtime]
~~~

## Sequence example

~~~mermaid
sequenceDiagram
  participant Visitor
  participant React
  participant API
  participant Model
  Visitor->>React: Enter weather values
  React->>API: POST /api/v1/risk/estimate
  API->>API: Validate source age
  API->>Model: Score demo indicator if fresh
  Model-->>API: Label, mode, limitations
  API-->>React: Explicit non-official response
  React-->>Visitor: Show experimental indicator and warnings
~~~

## Reproducibility

Train with \`python -m civicshield.ml.train --data PATH --output PATH\`; evaluated examples are NOT clinical or emergency standards. The risk API defaults to demo mode until configured otherwise.
