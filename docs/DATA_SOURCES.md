# Data sources and bookmarks

| Organization | URL | Current integration |
| --- | --- | --- |
| India Meteorological Department | https://mausam.imd.gov.in/ | Link only; not ingested |
| National Disaster Management Authority | https://ndma.gov.in/ | Link and contextual educational reference only |
| Central Water Commission | https://cwc.gov.in/ | Link only |
| Open Government Data Platform India | https://data.gov.in/ | Candidate dataset source; not ingested |
| OpenStreetMap | https://www.openstreetmap.org/copyright | Used as a map tile background in the web demo |

**Important:** Linked organizations have not endorsed this project. A link is not a license to reuse feed contents. Availability, authentication, terms, attribution, update frequency, spatial/temporal scope and quality must be verified before any live integration.

## Provenance

- \`/api/v1/weather/sample\`: synthetic, invented values.
- \`/api/v1/analytics/trends\`: synthetic, invented values.
- \`/api/v1/risk/estimate\`: user-supplied inputs; do not assume observed/verified.
- \`/api/v1/analytics/summary\`: counts of reports created in local app only.
- \`/api/v1/alerts\`: intentionally not connected, never equate \`[]\` with safety.

A real dataset would need provenance metadata, collection time, license, model-card review, and domain validation.
