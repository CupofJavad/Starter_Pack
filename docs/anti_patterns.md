# Known Anti-Patterns (Avoid)

- "Fixing" by weakening tests instead of correcting behavior
- Blanket try/except that hides the root cause
- Adding retries instead of fixing determinism
- Copy/pasting code from low-trust sources without verification
- Logging secrets or sensitive inputs
- Making large refactors during incident response
- Changing architecture without recording an ADR
