# Cursor Starter Package
A reusable “engineering operating system” for building small Python + React/Node apps with an AI agent in Cursor.

This repo makes three things consistent across projects:
1) How you bootstrap and verify environments
2) How you debug failures (disciplined + research-backed)
3) How you preserve memory across long gaps (conversation logs + error knowledge base + decisions)

────────────────────────────────────────────────────────────
Quick start
────────────────────────────────────────────────────────────
1) Fresh machine (Mac or Ubuntu server):
   make bootstrap-fresh
   (or non-interactive: make bootstrap-fresh-yes)

2) Normal setup (already have tools installed):
   make bootstrap

3) In Cursor, start your first chat with:
   Read and obey: .cursor/START_HERE.md

────────────────────────────────────────────────────────────
Environment landscape (canonical)
────────────────────────────────────────────────────────────
Local:
- MacBook Pro + Cursor
- Python-first backend and tooling
- React/Vite/TypeScript for web UI when needed

Remote:
- Ubuntu server (SSH) for deployments and long-running tasks

External services often used:
- Hugging Face (HF_TOKEN via env var only)
- NameSilo (NAMESILO_API_KEY via env var only)
- GitHub (GITHUB_TOKEN via env var only)
- Taskade (TASKADE_TOKEN via env var only)
- DigitalOcean Postgres (DO_PG_* env vars)
- Lunaverse server (SSH access via env vars)

Secrets policy:
- Never commit secrets
- Never paste real secrets into prompts
- Only reference env var NAMES (see .env.example)

────────────────────────────────────────────────────────────
Human + Agent collaboration model
────────────────────────────────────────────────────────────
The human provides:
- goals, constraints, preferences, judgment calls, domain context

The agent provides:
- architecture proposals, implementation, tests, research, disciplined debugging

Rules:
- The agent must read and follow the doctrine files in .cursor/
- The agent must prove changes with commands + tests
- Every fix must be documented when it’s “worth remembering”

────────────────────────────────────────────────────────────
Canonical development loop
────────────────────────────────────────────────────────────
1) Translate requirements into acceptance criteria (Given/When/Then)
2) Propose minimal architecture and file plan
3) Implement in small steps
4) Add tests
5) Run lint + typecheck + tests
6) Record learnings (Error KB, decision docs, context brief)

────────────────────────────────────────────────────────────
Failure-to-Fix Doctrine
────────────────────────────────────────────────────────────
When anything fails, the agent must follow:
.cursor/FAILURE_TO_FIX_PROTOCOL.md

One-command capture:
- Start a conversation log:
  make convo-new TITLE="My project session"
- Then on failure:
  make diagnose CMD="pytest -q" LOG="<path printed by convo-new>"

This will:
- snapshot environment fingerprint
- capture failure output
- record an Error KB entry
- optionally append to the raw conversation log

────────────────────────────────────────────────────────────
Memory systems
────────────────────────────────────────────────────────────
Working memory:
- .cursor/CONTEXT_BRIEF.md

Conversation vault:
- raw logs (private): .ops/conversations/raw/
- briefs (safe-ish): .ops/conversations/briefs/

Error Knowledge Base:
- .ops/error_kb/

Decisions:
- docs/decisions/

Promotion rules:
- Prevents a future failure? -> Error KB
- Explains a choice?        -> ADR (docs/decisions)
- Changes agent behavior?   -> CONTEXT_BRIEF

────────────────────────────────────────────────────────────
First prompt example: “Northern California gold prospecting app”
────────────────────────────────────────────────────────────

Paste this as your first message in Cursor:

Read and obey: .cursor/START_HERE.md

PROJECT GOAL
Build a small application to help identify high-potential gold deposits in Northern California.

HIGH-LEVEL OBJECTIVES
- Use only public/open data sources
- Prioritize explainability over black-box predictions
- Start as a local prototype (CLI or small GUI), then add a web UI if needed

CONSTRAINTS
- Open-source/free tools and data only
- Python-first for ingestion/analysis/modeling
- Mapping/visualization is required (layers, overlays)
- No paid APIs unless explicitly approved

REQUEST (NO CODE YET)
1) Restate the problem as acceptance criteria
2) Propose minimal architecture (modules, data flow)
3) List candidate public datasets (geology, hydrology, mining history) + limitations
4) Propose multiple approaches (rule-based scoring, spatial statistics, ML baseline)
5) Recommend a prototype scope that can be built in 1–2 sessions

────────────────────────────────────────────────────────────
Environment & Services
────────────────────────────────────────────────────────────
This starter pack supports a wide range of tools and services via environment variables:

**Server Management:**
- Cockpit (web-based server management)
- Lunaverse server (SSH access, LAN + Tailscale)
- pgAdmin (web-based database management)

**Databases:**
- Local Postgres (development)
- DigitalOcean Postgres (production)

**API Services:**
- Hugging Face (HF_TOKEN, HF_SSH_KEY_FINGERPRINT)
- GitHub (GITHUB_TOKEN)
- Taskade (TASKADE_TOKEN)
- NameSilo (NAMESILO_API_KEY, account URLs)

**Configuration:**
All credentials are provided via environment variables. See:
- `.env.example` for all available variables
- `docs/env-vars.md` for detailed documentation
- `docs/server-access.md` for SSH and server access
- `docs/db-access.md` for database connection examples

**Validation:**
Check required environment variables for different modes:
```bash
make env-check-local-dev    # Local development
make env-check-server-ops    # Server operations
make env-check-db-local      # Local Postgres
make env-check-db-do         # DigitalOcean Postgres
```

────────────────────────────────────────────────────────────
Dependency Sprawl Mitigation
────────────────────────────────────────────────────────────
To minimize disk usage and improve performance across projects:

**Python:**
- Prefer `uv` over `pip` (faster, better caching)
- `uv` uses a global cache for packages
- Falls back to `pip` if `uv` is not available

**Node:**
- Use `pnpm` (global store with deduplication)
- Avoid `npm` or `yarn` unless necessary
- `pnpm` significantly reduces `node_modules` size

**Best Practices:**
- Use the same Python version across projects (see `.python-version`)
- Share `pnpm` global store across all Node projects
- Use `uv` cache for faster Python dependency resolution
- Keep virtual environments project-local (`.venv/`)

────────────────────────────────────────────────────────────
Fresh Machine Setup (Final Boss)
────────────────────────────────────────────────────────────
Interactive:
  make bootstrap-fresh

Non-interactive:
  make bootstrap-fresh-yes

It will install baseline tooling, then run make bootstrap.
It will NOT manage secrets or deploy anything.