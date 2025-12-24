# Environment Variables Reference

This document describes all environment variables supported by the starter pack.
Values are never committed to git; only variable names are referenced in code.

---

## How to Read This Document

- Each variable notes its **intended environments**:
  - `(dev)` → primarily development/local use
  - `(prod)` → primarily production/remote use
  - `(both)` → applies to both dev and prod
- Unless otherwise stated, variables are **optional** and default to `None` or a sensible value.
- Secrets (passwords, tokens, API keys) must **never** be committed to git and are **redacted from logs**.

---

## Application Configuration

- `APP_ENV` `(both, optional)`:
  - Application environment (e.g., `dev`, `prod`, `test`)
  - Defaults to `dev` when unset.
- `LOG_LEVEL` `(both, optional)`:
  - Logging level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`)
  - Defaults to `INFO` when unset.
- `STRUCTURED_LOGGING` `(prod, optional)`:
  - When set to `true`, `1`, or `json`, enables JSON-structured logging in `app.logging_config`.
  - Defaults to human-readable text logs when unset.

---

## Server Configuration

- `SERVER_ADMIN_NAME` `(both, optional)`:
  - Name of the server administrator
- `SERVER_NAME` `(both, optional)`:
  - Name or identifier of the server

---

## Lunaverse Server Access

- `LUNAVERSE_HOST` `(prod, optional)`:
  - Hostname or IP address of the Lunaverse server
- `LUNAVERSE_SSH_USER` `(prod, optional)`:
  - SSH username for Lunaverse server access
- `LUNAVERSE_SSH_PORT` `(prod, optional)`:
  - SSH port (typically 22)
- `LUNAVERSE_SSH_PASSWORD` `(prod, secret, optional)`:
  - SSH password (optional; prefer SSH key authentication)
- `LUNAVERSE_SSH_TAILSCALE_HOST` `(prod, optional)`:
  - Tailscale hostname for Lunaverse (if using Tailscale VPN)

---

## Cockpit & pgAdmin

- `COCKPIT_URL` `(prod, optional)`:
  - Web URL for Cockpit server management interface
- `PGADMIN_URL` `(prod, optional)`:
  - Web URL for pgAdmin database management interface
- `PGADMIN_MASTER_PASSWORD` `(prod, secret, optional)`:
  - Master password for pgAdmin

---

## Local Postgres Database

- `POSTGRES_HOST` `(dev, optional)`:
  - Postgres server hostname (e.g., `localhost`)
- `POSTGRES_PORT` `(dev, optional)`:
  - Postgres server port (typically 5432)
- `POSTGRES_DB` `(dev, optional)`:
  - Database name
- `POSTGRES_USER` `(dev, optional)`:
  - Database user for application access
- `POSTGRES_PASSWORD` `(dev, secret, optional)`:
  - Password for `POSTGRES_USER`
- `POSTGRES_SUPERUSER` `(dev, optional)`:
  - Postgres superuser name (e.g., `postgres`)
- `POSTGRES_SUPERUSER_PASSWORD` `(dev, secret, optional)`:
  - Password for superuser
- `POSTGRES_ALT_USER` `(dev, optional)`:
  - Alternative database user (if needed)
- `POSTGRES_ALT_PASSWORD` `(dev, secret, optional)`:
  - Password for alternative user

---

## Default Admin Credentials

- `DEFAULT_ADMIN_EMAIL` `(prod, optional)`:
  - Default administrator email address
- `DEFAULT_ADMIN_PASSWORD` `(prod, secret, optional)`:
  - Default administrator password
- `DEFAULT_ADMIN_ROLE` `(prod, optional)`:
  - Default administrator role name

---

## Application User

- `LUNAVERSE_APP_USER` `(prod, optional)`:
  - Application-specific user account name
- `LUNAVERSE_APP_PASSWORD` `(prod, secret, optional)`:
  - Password for application user

---

## API Tokens

- `GITHUB_TOKEN` `(both, secret, optional)`:
  - GitHub personal access token or OAuth token
- `HF_TOKEN` `(both, secret, optional)`:
  - Hugging Face API token
- `HF_SSH_KEY_FINGERPRINT` `(both, optional)`:
  - SSH key fingerprint for Hugging Face SSH access

---

## DigitalOcean Postgres

- `DO_PG_HOST` `(prod, optional)`:
  - DigitalOcean Postgres cluster hostname
- `DO_PG_PORT` `(prod, optional)`:
  - DigitalOcean Postgres port (typically 25060)
- `DO_PG_USER` `(prod, optional)`:
  - DigitalOcean Postgres username
- `DO_PG_PASSWORD` `(prod, secret, optional)`:
  - DigitalOcean Postgres password
- `DO_PG_SSLMODE` `(prod, optional)`:
  - SSL mode (e.g., `require`, `verify-full`)

---

## Taskade

- `TASKADE_TOKEN` `(both, secret, optional)`:
  - Taskade API token

---

## NameSilo

- `NAMESILO_API_KEY` `(both, secret, optional)`:
  - NameSilo API key for domain management
- `NAMESILO_ACCOUNT_URL` `(both, optional)`:
  - NameSilo account dashboard URL
- `NAMESILO_SITE_BUILDER_URL` `(both, optional)`:
  - NameSilo site builder URL

---

## Security Notes

- All password and token values are automatically redacted from logs via `app.logging_config.RedactingFilter`
- Never commit `.env` files to git
- Use `.env.example` as a template (with blank/placeholder values)
- Prefer SSH key authentication over passwords when possible
- Rotate credentials regularly
- For production, consider using a dedicated **secrets manager** (e.g., cloud provider service)
  that injects values via environment variables rather than storing them on disk.

---

## Validation

Use the environment validation script to check required variables:

```bash
make env-check-local-dev    # Local development
make env-check-server-ops    # Server operations
make env-check-db-local      # Local Postgres
make env-check-db-do         # DigitalOcean Postgres
```

