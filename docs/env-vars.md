# Environment Variables Reference

This document describes all environment variables supported by the starter pack.
Values are never committed to git; only variable names are referenced in code.

---

## Application Configuration

- `APP_ENV`: Application environment (e.g., `dev`, `prod`, `test`)
- `LOG_LEVEL`: Logging level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`)

---

## Server Configuration

- `SERVER_ADMIN_NAME`: Name of the server administrator
- `SERVER_NAME`: Name or identifier of the server

---

## Lunaverse Server Access

- `LUNAVERSE_HOST`: Hostname or IP address of the Lunaverse server
- `LUNAVERSE_SSH_USER`: SSH username for Lunaverse server access
- `LUNAVERSE_SSH_PORT`: SSH port (typically 22)
- `LUNAVERSE_SSH_PASSWORD`: SSH password (optional; prefer SSH key authentication)
- `LUNAVERSE_SSH_TAILSCALE_HOST`: Tailscale hostname for Lunaverse (if using Tailscale VPN)

---

## Cockpit & pgAdmin

- `COCKPIT_URL`: Web URL for Cockpit server management interface
- `PGADMIN_URL`: Web URL for pgAdmin database management interface
- `PGADMIN_MASTER_PASSWORD`: Master password for pgAdmin

---

## Local Postgres Database

- `POSTGRES_HOST`: Postgres server hostname (e.g., `localhost`)
- `POSTGRES_PORT`: Postgres server port (typically 5432)
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user for application access
- `POSTGRES_PASSWORD`: Password for `POSTGRES_USER`
- `POSTGRES_SUPERUSER`: Postgres superuser name (e.g., `postgres`)
- `POSTGRES_SUPERUSER_PASSWORD`: Password for superuser
- `POSTGRES_ALT_USER`: Alternative database user (if needed)
- `POSTGRES_ALT_PASSWORD`: Password for alternative user

---

## Default Admin Credentials

- `DEFAULT_ADMIN_EMAIL`: Default administrator email address
- `DEFAULT_ADMIN_PASSWORD`: Default administrator password
- `DEFAULT_ADMIN_ROLE`: Default administrator role name

---

## Application User

- `LUNAVERSE_APP_USER`: Application-specific user account name
- `LUNAVERSE_APP_PASSWORD`: Password for application user

---

## API Tokens

- `GITHUB_TOKEN`: GitHub personal access token or OAuth token
- `HF_TOKEN`: Hugging Face API token
- `HF_SSH_KEY_FINGERPRINT`: SSH key fingerprint for Hugging Face SSH access

---

## DigitalOcean Postgres

- `DO_PG_HOST`: DigitalOcean Postgres cluster hostname
- `DO_PG_PORT`: DigitalOcean Postgres port (typically 25060)
- `DO_PG_USER`: DigitalOcean Postgres username
- `DO_PG_PASSWORD`: DigitalOcean Postgres password
- `DO_PG_SSLMODE`: SSL mode (e.g., `require`, `verify-full`)

---

## Taskade

- `TASKADE_TOKEN`: Taskade API token

---

## NameSilo

- `NAMESILO_API_KEY`: NameSilo API key for domain management
- `NAMESILO_ACCOUNT_URL`: NameSilo account dashboard URL
- `NAMESILO_SITE_BUILDER_URL`: NameSilo site builder URL

---

## Security Notes

- All password and token values are automatically redacted from logs
- Never commit `.env` files to git
- Use `.env.example` as a template (with blank/placeholder values)
- Prefer SSH key authentication over passwords when possible
- Rotate credentials regularly

---

## Validation

Use the environment validation script to check required variables:

```bash
make env-check-local-dev    # Local development
make env-check-server-ops    # Server operations
make env-check-db-local      # Local Postgres
make env-check-db-do         # DigitalOcean Postgres
```

