# Source provenance, licenses and bookmarks

| Provider | URL | Current behavior |
| --- | --- | --- |
| India Meteorological Department (IMD) | https://mausam.imd.gov.in/ | External official homepage bookmark only; **no feed connected** |
| National Disaster Management Authority (NDMA) | https://ndma.gov.in/ | Official homepage bookmark and reference for manually authored educational summaries |
| Central Water Commission (CWC) | https://cwc.gov.in/ | Official homepage bookmark only |
| Open Government Data India | https://data.gov.in/ | Candidate dataset discovery bookmark; no data shipped |
| Open-Meteo | https://open-meteo.com/en/docs | Optional **modeled weather** fetched on demand via server; no official alerts |
| OpenStreetMap | https://www.openstreetmap.org/copyright | Tiled map background with attribution; external third-party tile requests |

Open-Meteo's free public API is intended for non-commercial usage with applicable daily/hourly/minute quotas and CC BY 4.0 attribution. Follow its terms: https://open-meteo.com/en/terms . Do not infer that official Indian authorities endorse or validate these model outputs.

## Data-type provenance

- \`/api/v1/weather/sample\`: synthetic invented example, not live.
- \`/api/v1/weather/live\`: third-party modeled gridded weather, opt-in. Endpoint rounds requested coordinates to 2 decimal places before external submission; timestamps, cache state and license URL included. It does not use a government alert API.
- \`/api/v1/risk/estimate\`: manually supplied values; output is experiment only.
- \`/api/v1/analytics/trends\`: **actual locally submitted reports counted by date**, but reports are *unverified* and are not observed disaster events.
- \`/api/v1/analytics/summary\`: locally stored report status/category counts only.
- \`/api/v1/alerts\`: connection_state not_connected; empty array means nothing about actual warning status.
- \`/api/v1/assistant/knowledge\`: manually authored source-linked summaries, not up-to-date advisories, with curated date per record.
- \`/api/v1/assistant/ask\`: embedded educational translations; not automated external retrieval.

## Historical labeled training data

No authoritative labeled floods/injuries/heat events are included. The local train command rejects invalid, too-small or single-class input and evaluates chronological holdouts; these checks do not guarantee correct outcome labels, nonleaky features, regional transfer, calibration or real-world safety. Document origin, scope, consent, sample period and license for any real dataset you add.
