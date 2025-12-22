# Contributing Guide

Thank you for contributing. This repository values correctness,
clarity, and long-term maintainability over speed or cleverness.

---

## Ground Rules

- Keep changes small and focused
- Prefer explicitness over magic
- Follow existing structure and conventions
- If behavior changes, tests must change
- If architecture changes, document it

---

## Local Development Setup

1. Clone the repository
   git clone <repo-url>
   cd <repo>

2. Bootstrap the environment
   make bootstrap

This will:
- Create a Python virtual environment
- Install development dependencies
- Initialize ops directories
- Run baseline checks

---

## Required Checks (Must Pass)

Before opening a pull request, run:

. .venv/bin/activate
pytest -q
ruff check .
pyright

If any fail, fix them before proceeding.

---

## Failure Handling Expectations

If something breaks:
- Do NOT weaken tests to make them pass
- Do NOT apply random fixes without reproduction
- Follow .cursor/FAILURE_TO_FIX_PROTOCOL.md

Preferred workflow:
make convo-new TITLE="short description"
make diagnose CMD="<failing command>" LOG="<raw log path>"

---

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference issues or error signatures when applicable
- Prefer logical commits over large mixed changes

Examples:
fix: correct path handling on macOS
test: add regression test for config parsing
docs: clarify bootstrap expectations

---

## Documentation and Memory

If your change introduces:
- A new architectural decision → add an ADR in docs/decisions/
- A recurring bug pattern → update .ops/error_kb/
- A new agent behavior rule → update .cursor/CONTEXT_BRIEF.md

Knowledge should be preserved, not rediscovered.

---

## What Not to Do

- Do not commit secrets
- Do not log sensitive values
- Do not bypass CI or quality checks
- Do not introduce breaking changes without discussion

---

## Questions

If something is unclear:
- Read the files in .cursor/
- Check existing ADRs
- Ask before making large changes

