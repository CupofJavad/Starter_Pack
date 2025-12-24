## Industry Standards in This Starter Pack

This repo is intentionally small, but it still aligns with several widely used practices.
This document maps those **industry-standard ideas** to the **concrete things in this repo**.

---

## 1. Environment & Secrets Management

**Industry practices**
- Follow Twelve-Factor principles for configuration: **config in the environment**, not in code.
- Keep the **fresh-clone experience** simple: minimal required variables, sensible defaults.
- Treat secrets as **runtime-only**, never committed, and **validate** configuration explicitly.

**How this repo implements it**
- All configuration is read from environment variables via `app.settings.Settings.load()`.
- `.env` is **gitignored**; `.env.example` is the canonical template.
- `docs/env-vars.md` documents all supported variables and marks which ones are dev- vs prod-oriented.
- `make env-check-*` targets (backed by `.ops/scripts/check_env.py`) validate environment modes:
  - `make env-check-local-dev`
  - `make env-check-server-ops`
  - `make env-check-db-local`
  - `make env-check-db-do`

**What to copy into your own projects**
- Keep **all config** in env vars (or a secret manager that exposes them as env vars).
- Maintain an explicit `env-vars` doc and `.env.example` with:
  - Clear indication of **dev / prod / both**.
  - Which vars are **required vs optional**.
- Add a simple `make env-check-*` (or similar) command that fails fast when misconfigured.

---

## 2. Logging, Observability & Redaction

**Industry practices**
- Centralized, consistent logging configuration.
- **Redact secrets** and sensitive values before they leave the process.
- Prefer **structured logs** (e.g., JSON) when integrating with log aggregation tools.

**How this repo implements it**
- `app.logging_config` provides:
  - `RedactingFilter` that automatically redacts values for all keys in `REDACT_KEYS`.
  - `configure_logging(level)` to configure application logging in one place.
- The logging decision record (`docs/decisions/0002-logging-approach.md`) captures the rationale.
- Optional **structured logging**:
  - The `STRUCTURED_LOGGING` environment variable (e.g. `STRUCTURED_LOGGING=true` or `STRUCTURED_LOGGING=json`)
    enables JSON-formatted logs via a dedicated formatter.

**What to copy into your own projects**
- Centralize logging setup in a single module (like `logging_config`).
- Maintain a list of **sensitive keys** (`REDACT_KEYS`) and apply a filter to the root logger.
- Provide an **opt-in structured logging mode** for production (JSON), defaulting to human-readable logs in dev.

---

## 3. Testing & Quality Gates

**Industry practices**
- Follow a **testing pyramid**: fast unit tests at the base, selective integration tests on top.
- Enforce a **minimal quality gate**:
  - Linting
  - Type checking
  - Test suite
- Make the quality gate **one command** so it is easy to run locally and in CI.

**How this repo implements it**
- `tests/` includes:
  - Smoke tests (`test_smoke.py`)
  - Settings tests (`test_settings.py`)
  - Logging redaction tests (`test_logging_redaction.py`)
  - Environment validation tests (`test_check_env.py`)
- `docs/TESTING_GUIDE.md` and `FINALIZATION_CHECKLIST.md` describe how to run:
  - `pytest tests/ -v`
  - `ruff check .`
  - `pyright`
- `make quality` (added in the `Makefile`) bundles these into a **single quality gate** command.

**What to copy into your own projects**
- Establish a small but strict **baseline** for every repo:
  - `pytest` for tests
  - `ruff` (or similar) for linting
  - `pyright` (or similar) for type checking
- Add a `make quality` (or equivalent) that runs all three.
- Ensure tests **do not require real secrets**; they should run in a fresh clone with no `.env`.

---

## 4. Architecture Decisions & Documentation

**Industry practices**
- Use **Architecture Decision Records (ADRs)** to document important, long-lived decisions.
- Keep ADRs **short and searchable**: Context → Decision → Consequences.
- Treat documentation as part of the system, not an afterthought.

**How this repo implements it**
- `docs/decisions/` stores ADRs (e.g., tech stack, logging approach, credentials policy).
- `docs/decisions/README.md` defines a simple ADR template:
  - Context
  - Decision
  - Alternatives Considered
  - Consequences
- `docs/industry_standards.md` (this file) summarizes how the repo aligns with common norms.
- `.ops/error_kb` is used as an **error knowledge base**, with a template described in
  `docs/error_kb_template.md` to standardize entries.

**What to copy into your own projects**
- Create a `docs/decisions/` folder and stick to a small ADR template.
- When you change tooling, architecture, or security posture, **write or update an ADR**.
- Capture recurring errors or incidents using a lightweight template (see `docs/error_kb_template.md`).

---

## 5. Developer Experience & Onboarding

**Industry practices**
- Make the **first 15 minutes** with a repo smooth:
  - Clear prerequisites
  - One-command bootstrap
  - A short, accurate README map
- Provide a repeatable **“fresh clone”** scenario to verify nothing depends on hidden state.

**How this repo implements it**
- `README.md` explains:
  - What the repo is for
  - How to clone it
  - How to run `make bootstrap` and activate the virtualenv
- `make bootstrap` sets up:
  - Virtual environment
  - Dependencies
  - Operational memory directories under `.ops/`
  - A basic test / tool check
- `QUICK_TEST.md`, `TESTING_GUIDE.md`, and `FINALIZATION_CHECKLIST.md` document:
  - How to verify imports and venv
  - How to run tests and quality checks
  - How to simulate a **fresh-clone** run

**What to copy into your own projects**
- Ensure your README answers, quickly:
  - “What is this?”
  - “How do I run it in 1–2 commands?”
  - “How do I know it’s working?”
- Maintain a small **DX checklist** in your docs or issues for new projects cloned from this starter.
- Regularly re-run the **fresh clone test** from a clean directory to ensure onboarding stays smooth.


