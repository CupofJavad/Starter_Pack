SHELL := /bin/bash
PY := python3

.PHONY: help bootstrap bootstrap-fresh bootstrap-fresh-yes verify-setup env-fingerprint diagnose kb-record \
        convo-new convo-append convo-brief env-check-local-dev env-check-server-ops \
        env-check-db-local env-check-db-do quality

help:
	@echo "Targets:"
	@echo "  bootstrap                 Setup venv, install deps, init ops dirs, run checks"
	@echo "  bootstrap-fresh           Fresh machine install (interactive) then bootstrap"
	@echo "  bootstrap-fresh-yes       Fresh machine install (non-interactive) then bootstrap"
	@echo "  verify-setup              Verify that setup is complete (for first-time users)"
	@echo "  quality                   Run standard quality gate (ruff, pyright, pytest)"
	@echo "  env-fingerprint           Print local tool/runtime fingerprints"
	@echo "  env-check-local-dev      Check env vars for local development"
	@echo "  env-check-server-ops     Check env vars for server operations"
	@echo "  env-check-db-local       Check env vars for local Postgres"
	@echo "  env-check-db-do          Check env vars for DigitalOcean Postgres"
	@echo "  diagnose CMD='<cmd>' LOG=<optional_convo_log>  Capture failure evidence + KB entry"
	@echo "  kb-record LOG=<path>      Record a failure log into Error KB"
	@echo "  convo-new TITLE='...'     Create a new raw conversation log"
	@echo "  convo-append LOG=<path> SRC=<path|-> Append text to a raw log"
	@echo "  convo-brief LOG=<path>    Generate a scrubbed brief from a raw log"

bootstrap:
	@echo "== Bootstrap: validating environment =="
	@$(PY) --version || (echo "Python missing" && exit 1)

	@echo "== Bootstrap: preparing Python environment =="
	@$(PY) -m venv .venv
	@. .venv/bin/activate && python -m pip install --upgrade pip

	@if command -v uv >/dev/null 2>&1; then \
		echo "Using uv for dependency install"; \
		. .venv/bin/activate && uv pip install -e ".[dev]"; \
	else \
		echo "uv not found, falling back to pip"; \
		. .venv/bin/activate && pip install -e ".[dev]"; \
	fi

	@echo "== Bootstrap: initializing ops directories =="
	@mkdir -p .ops/error_kb/cases
	@mkdir -p .ops/conversations/raw
	@mkdir -p .ops/conversations/briefs
	@mkdir -p .ops/logs

	@echo "== Bootstrap: environment fingerprint =="
	@. .venv/bin/activate && python .ops/scripts/fingerprint_env.py > .ops/logs/bootstrap_env.txt || true

	@echo "== Bootstrap: baseline checks =="
	@. .venv/bin/activate && pytest -q || true
	@. .venv/bin/activate && ruff --version || true
	@. .venv/bin/activate && pyright --version || true

	@echo ""
	@echo "== Bootstrap complete =="
	@echo "Next steps:"
	@echo "1. Activate the environment: source .venv/bin/activate"
	@echo "2. Verify setup: make verify-setup"
	@echo "3. Open Cursor and use the prompt from FIRST_PROMPT.md"

bootstrap-fresh:
	@bash .ops/scripts/bootstrap_fresh.sh

bootstrap-fresh-yes:
	@YES=1 bash .ops/scripts/bootstrap_fresh.sh

verify-setup:
	@. .venv/bin/activate && python .ops/scripts/verify_setup.py || (echo "Note: Run 'make bootstrap' first if verification fails" && exit 1)

env-fingerprint:
	@. .venv/bin/activate && python .ops/scripts/fingerprint_env.py

kb-record:
	@if [ -z "$(LOG)" ]; then echo "Missing LOG=<path_to_error_log.txt>"; exit 2; fi
	@. .venv/bin/activate && python .ops/scripts/record_failure.py "$(LOG)"

convo-new:
	@if [ -z "$(TITLE)" ]; then echo "Missing TITLE='...'" ; exit 2; fi
	@$(PY) .ops/scripts/convo_new.py "$(TITLE)"

convo-append:
	@if [ -z "$(LOG)" ]; then echo "Missing LOG=<path_to_raw_log.txt>"; exit 2; fi
	@if [ -z "$(SRC)" ]; then echo "Missing SRC=<path_to_text_file_or_->"; exit 2; fi
	@$(PY) .ops/scripts/convo_append.py "$(LOG)" "$(SRC)"

convo-brief:
	@if [ -z "$(LOG)" ]; then echo "Missing LOG=<path_to_raw_log.txt>"; exit 2; fi
	@$(PY) .ops/scripts/convo_brief.py "$(LOG)"

diagnose:
	@if [ -z "$(CMD)" ]; then echo "Missing CMD='<command to reproduce failure>'"; exit 2; fi
	@. .venv/bin/activate && python .ops/scripts/diagnose.py --cmd "$(CMD)" $(if $(LOG),--convo-log "$(LOG)",)

env-check-local-dev:
	@. .venv/bin/activate && python .ops/scripts/check_env.py local-dev

env-check-server-ops:
	@. .venv/bin/activate && python .ops/scripts/check_env.py server-ops

env-check-db-local:
	@. .venv/bin/activate && python .ops/scripts/check_env.py db-local

env-check-db-do:
	@. .venv/bin/activate && python .ops/scripts/check_env.py db-do

quality:
	@. .venv/bin/activate && ruff check .
	@. .venv/bin/activate && pyright
	@. .venv/bin/activate && pytest tests/ -q

