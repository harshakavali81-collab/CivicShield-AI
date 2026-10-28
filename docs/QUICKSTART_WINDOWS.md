# Windows quick start — CivicShield AI portfolio demo

This guide works on Windows 10/11 with [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) running Linux containers, and Windows PowerShell or PowerShell 7.

## Clone

In PowerShell:

\`\`\`powershell
git clone https://github.com/harshakavali81-collab/CivicShield-AI.git
Set-Location CivicShield-AI
\`\`\`

## Start the complete local stack

\`\`\`powershell
.\scripts\start-local.ps1
\`\`\`

The script copies \`.env.example\` into the **gitignored** \`.env\` if necessary, generates a random 48-character hexadecimal local PostgreSQL password if none is configured, preserves an existing password, starts Docker containers, and prints local links. It does not send credentials to ChatGPT, GitHub, Render or any model service.

If Windows restricts script execution, use a PowerShell session whose policy is authorized by your device administrator, or run the equivalent manual steps: copy \`.env.example\` to \`.env\`, set a strong \`POSTGRES_PASSWORD\`, then run \`docker compose up --build -d\`.

## Open

- Dashboard: http://localhost:5173
- OpenAPI documentation: http://localhost:8000/docs
- Software readiness: http://localhost:8000/api/ready
- Scenario Lab: select **Scenario lab** in the dashboard
- Official sources: linked authority homepages, **not** a connected warning feed

## Check and shut down

\`\`\`powershell
docker compose ps
docker compose logs --tail=80 api
python -m scripts.smoke_demo --url http://localhost:8000
.\scripts\stop-local.ps1
\`\`\`

Stopping containers retains the database volume. Avoid \`docker compose down -v\` or deleting local backups without an intentional data-retention decision.

## Notes and limitations

- No IMD/CWC account, actual disaster prediction or public deployment is created.
- The demo's citizen-report intake is disabled by default.
- The Open-Meteo modeled weather connection is also disabled until explicitly enabled and its terms are reviewed.
- The Scenario Lab uses invented data and **does not** write into the incident database.
- Never reuse a local development password or demo reviewer key for a public website.
