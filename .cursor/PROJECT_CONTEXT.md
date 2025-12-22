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
- Hugging Face (HF_TOKEN via env var only)
- NameSilo (NAMESILO_API_KEY via env var only)

## Secrets & Credentials Policy
- Never hardcode secrets.
- Never commit secrets.
- Code may only reference env var NAMES (not values).
- Logs must redact secrets.
- If creds missing, fail with a clear message explaining required env vars.

## Common Env Vars (names only)
- HF_TOKEN
- NAMESILO_API_KEY
- UBUNTU_HOST
- UBUNTU_USER
- UBUNTU_SSH_KEY_PATH
- APP_ENV
- LOG_LEVEL
