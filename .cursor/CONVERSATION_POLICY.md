# Conversation Vault Policy

- Raw conversation logs live in .ops/conversations/raw/ (gitignored by default).
- Briefs live in .ops/conversations/briefs/ (intended to be scrubbed/safe-ish).
- Never store real secrets in raw logs. If secrets appear, redact them before archiving.

How to use in Cursor:
- Start every session by referencing .cursor/START_HERE.md
- Keep .cursor/CONTEXT_BRIEF.md updated when a session ends
- Generate a brief from raw logs if resuming after a long gap

Knowledge promotion rules:
- Raw logs = volatile memory
- Briefs = working memory
- Error KB + ADRs = long-term memory

If knowledge:
- prevents a future failure → Error KB
- explains a decision → ADR
- affects how agent should reason → CONTEXT_BRIEF
