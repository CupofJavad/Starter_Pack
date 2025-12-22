ADVANCED ERROR INTELLIGENCE MODE

- Maintain Error KB at .ops/error_kb/
- When failures occur:
  1) reproduce deterministically
  2) capture output, versions, OS info
  3) compute stable error signature
  4) check Error KB for known fix pattern
  5) if unknown, propose fix using trusted sources only (official docs, GitHub issues/PRs, release notes)
  6) apply minimal patch + add regression test
  7) rerun full pipeline until green OR blocked

Never paste random code from low-trust sources.
Never hide symptoms by weakening tests.
