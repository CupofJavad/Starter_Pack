# Error Knowledge Base (Error KB)

Purpose:
Turn bugs into permanent immunity.

Structure:
- error_index.json maps signatures -> case folders
- cases/<signature>/ contains:
  - symptoms.md
  - root_cause.md
  - fix.md
  - regression_test.md

Workflow:
- When failure occurs, capture output (use make diagnose)
- record_failure.py creates a case skeleton
- When fixed, fill in root cause and fix, and add regression tests
