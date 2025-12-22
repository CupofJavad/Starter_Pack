# Decision: Default Tech Stack
Date: 2025-12-22
Status: Accepted

Context:
We build many small local + web apps and need speed, consistency, and reuse.

Decision:
Default to:
- Python for backend/automation; FastAPI where web APIs are needed
- React + Vite + TypeScript for web UI
- uv (preferred) or pip for Python deps; ruff + pyright + pytest for quality
- pnpm for Node dependency management if Node is used

Alternatives Considered:
- Poetry (fine, slower than uv in practice)
- npm/yarn (pnpm is faster + global store dedupe)

Consequences:
+ Fast iteration and consistent quality checks
- Some teams may prefer different tools; record overrides as ADRs
