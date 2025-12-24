## Error Knowledge Base Entry Template

Use this template when adding a new case under `.ops/error_kb/cases/`.
Keep entries short, factual, and focused on **helping future-you fix it faster**.

---

### Title

- Short, descriptive summary of the issue.
  - Example: `Bootstrap fails: ModuleNotFoundError: No module named 'app'`

### Date

- When this incident or error was investigated.

### Context

- Where and how it happened:
  - Environment (local, server, CI)
  - Command that was run
  - Relevant configuration (e.g., presence/absence of `.env`, venv, DB)

### Impact

- Who or what was affected?
- How bad was it? (e.g., “Bootstrap blocked for all developers”, “Only a one-off script failed”)

### Root Cause

- The underlying cause in one or two sentences.
- Include links to code or docs if helpful.

### Resolution / Fix

- What you did to fix it.
- Include commands, patches, or configuration changes.

### Prevention / Follow-Ups

- How to reduce the chance of recurrence:
  - Extra tests
  - Doc updates
  - New Make targets
  - ADRs or policy changes

### References

- Links to:
  - GitHub issues / PRs
  - ADRs
  - External docs (if any)


