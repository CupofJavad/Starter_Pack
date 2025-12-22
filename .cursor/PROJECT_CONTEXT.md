# Project Context (Canonical)

## Primary Dev Environment
- IDE: Cursor
- Local: MacBook Pro (macOS)
- Remote: Ubuntu server (SSH)
- Typical projects: small local tools + small web apps

## Preferred Stack
- Web UI: React + Vite + TypeScript
- Node backend: Node LTS + TypeScript (Fastify/Express acceptable)
- Python backend/API: FastAPI + pydantic
- Python local GUI: PySide6 (Qt) or DearPyGui for rapid tools
- DB: SQLite by default; Postgres if needed

## External Services Often Used
- Hugging Face (HF_TOKEN, HF_SSH_KEY_FINGERPRINT via env vars)
- NameSilo (NAMESILO_API_KEY, NAMESILO_ACCOUNT_URL, NAMESILO_SITE_BUILDER_URL via env vars)
- GitHub (GITHUB_TOKEN via env var)
- Taskade (TASKADE_TOKEN via env var)
- DigitalOcean Postgres (DO_PG_* env vars)
- Lunaverse server (SSH access via LUNAVERSE_* env vars)
- Cockpit (COCKPIT_URL via env var)
- pgAdmin (PGADMIN_URL, PGADMIN_MASTER_PASSWORD via env vars)

## Secrets & Credentials Policy
- Never hardcode secrets.
- Never commit secrets.
- Code may only reference env var NAMES (not values).
- Logs must redact secrets.
- If creds missing, fail with a clear message explaining required env vars.

## Common Env Vars (names only)
- APP_ENV, LOG_LEVEL
- SERVER_ADMIN_NAME, SERVER_NAME
- LUNAVERSE_HOST, LUNAVERSE_SSH_USER, LUNAVERSE_SSH_PORT, LUNAVERSE_SSH_TAILSCALE_HOST
- COCKPIT_URL, PGADMIN_URL, PGADMIN_MASTER_PASSWORD
- POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
- POSTGRES_SUPERUSER, POSTGRES_SUPERUSER_PASSWORD
- DO_PG_HOST, DO_PG_PORT, DO_PG_USER, DO_PG_PASSWORD, DO_PG_SSLMODE
- GITHUB_TOKEN, HF_TOKEN, HF_SSH_KEY_FINGERPRINT
- TASKADE_TOKEN
- NAMESILO_API_KEY, NAMESILO_ACCOUNT_URL, NAMESILO_SITE_BUILDER_URL
- DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_ROLE
- LUNAVERSE_APP_USER, LUNAVERSE_APP_PASSWORD

See `.env.example` and `docs/env-vars.md` for complete list.
