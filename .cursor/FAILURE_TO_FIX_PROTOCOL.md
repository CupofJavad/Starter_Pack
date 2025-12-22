# Failure-to-Fix Protocol (Canonical)

OBJECTIVE
When any script/build/test fails, follow a disciplined, research-backed workflow that:
- reproduces deterministically
- explores multiple solution paths
- selects the best fix using industry-standard practices
- proves the fix with tests and prevents regressions
- records the outcome into the Error Knowledge Base (Error KB)

PRINCIPLES
- Correctness > speed; prefer minimal safe changes.
- Never "guess-fix" without reproduction + evidence.
- Prefer authoritative sources: official docs, release notes, security advisories, and primary GitHub issues/PRs.
- No copy-paste from low-trust sources. If code is used, justify trust and add tests.

PHASE 0 — CAPTURE & REPRODUCE (NO FIXING YET)
1) Capture context:
   - exact command(s) run
   - full error output/stack trace
   - OS + runtime versions and key package versions
2) Reduce to a deterministic reproduction:
   - smallest command that fails consistently
3) Compute an error signature:
   - stable fingerprint based on exception type + key message lines + module/package
4) Check local resources first:
   - repo docs / RUNBOOK
   - Error KB signature match
   - recent diffs and breaking changes
   - lockfiles and pinned versions

PHASE 1 — HYPOTHESES (MULTIPLE PATHS REQUIRED)
Generate at least 3 root-cause hypotheses, each with:
- Why it could be true
- Evidence that would confirm/deny it
- The lowest-cost test to validate it

PHASE 2 — RESEARCH (LOCAL + ONLINE, KEYWORDS FIRST)
A) Local research:
- search codebase for error strings and modules
- inspect configs (pyproject, lockfiles, CI) and recent commits

B) Online research (authoritative-first):
- extract keywords: package, version, exception type, message excerpt
- generate 2–5 targeted queries:
  - "<package> <version> <error message excerpt>"
  - "<exception type> <module> <symptom>"
  - "<tool> (uv/ruff/pnpm/vite/pytest) <error>"
- prioritize sources:
  1) official docs / release notes
  2) GitHub issues/PRs in the relevant repo
  3) reputable maintainer blogs
  4) StackOverflow only as last resort; verify against primary sources

PHASE 3 — SOLUTION PATHS (COMPARE OPTIONS)
For each fix path, evaluate:
- Correctness, Security, Maintainability, Reproducibility (Mac + Ubuntu + CI), Scope/Risk, Time-to-validate, Standards alignment

Rank solution paths and choose the best one.
If uncertain, choose the smallest reversible change that increases information (diagnostic logging/tests).

PHASE 4 — APPLY FIX (MINIMAL + VERIFIED)
- implement minimal patch
- add regression tests
- run full pipeline: lint/format + typecheck + tests (+ integration)
- if still failing: return to PHASE 1 with new evidence (no random thrashing)

PHASE 5 — RECORD LEARNING
- update Error KB: symptoms, root cause, fix, regression test notes
- update CONTEXT_BRIEF if decisions changed
- commit with Conventional Commits and reference the error signature
