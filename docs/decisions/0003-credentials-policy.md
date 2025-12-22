# Decision: Credentials via Environment Variables Only
Date: 2025-12-22
Status: Accepted

Context:
Frequent use of Hugging Face and NameSilo requires credentials.

Decision:
All credentials are provided via environment variables.
No secrets are committed to git or placed in prompts.

Alternatives Considered:
- Hardcoding in config files (unsafe)
- Committing encrypted secrets (still risky; requires key management)

Consequences:
+ Secure, portable, compatible with CI and servers
- Requires consistent local env management (.env, direnv, etc.)
