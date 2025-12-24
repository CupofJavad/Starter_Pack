# Decision: Structured Logging + Redaction
Date: 2025-12-22
Status: Accepted

Context:
We need logs that help debugging and do not leak secrets.

Decision:
Use Python logging with a redaction filter (at minimum).
Prefer structured JSON logging later if needed, exposed as an **opt-in mode**
controlled via the `STRUCTURED_LOGGING` environment variable.

Alternatives Considered:
- No logging discipline (too costly long-term)
- Full OpenTelemetry everywhere (overkill for small apps by default)

Consequences:
+ Safer logs, easier debugging
+ Ability to switch to JSON logs in environments that benefit from structured logging
- Slight setup overhead
