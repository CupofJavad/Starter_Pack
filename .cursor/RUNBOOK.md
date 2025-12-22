# Runbook

## Python (preferred: uv, fallback: pip)
Bootstrap:
- make bootstrap

Common commands:
- . .venv/bin/activate
- pytest -q
- ruff check .
- ruff format .
- pyright

## Conversations / Diagnostics
- make convo-new TITLE="Session title"
- make diagnose CMD="pytest -q" LOG="<raw log path>"

## Ubuntu Server
SSH:
- ssh -i "$UBUNTU_SSH_KEY_PATH" "$UBUNTU_USER@$UBUNTU_HOST"

Sync example (rsync):
- rsync -av --exclude .venv --exclude node_modules ./ "$UBUNTU_USER@$UBUNTU_HOST:~/app/"
