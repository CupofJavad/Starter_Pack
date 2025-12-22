# Database Access Guide

This guide covers accessing Postgres databases, both local and DigitalOcean managed instances.

---

## Local Postgres

### psql Command Line

Connect to local Postgres:

```bash
psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB}
```

Or using connection string:

```bash
psql "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
```

### Superuser Access

For administrative tasks:

```bash
psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_SUPERUSER} -d postgres
```

### Common Operations

List databases:
```sql
\l
```

Connect to a database:
```sql
\c ${POSTGRES_DB}
```

List tables:
```sql
\dt
```

Exit:
```sql
\q
```

---

## DigitalOcean Postgres

### Connection String

DigitalOcean Postgres requires SSL:

```bash
psql "postgresql://${DO_PG_USER}:${DO_PG_PASSWORD}@${DO_PG_HOST}:${DO_PG_PORT}/defaultdb?sslmode=${DO_PG_SSLMODE:-require}"
```

### SSL Certificate (if verify-full)

If `DO_PG_SSLMODE=verify-full`, download the CA certificate from DigitalOcean dashboard and use:

```bash
psql "postgresql://${DO_PG_USER}:${DO_PG_PASSWORD}@${DO_PG_HOST}:${DO_PG_PORT}/defaultdb?sslmode=verify-full&sslrootcert=/path/to/ca-certificate.crt"
```

### Connection Pooling (Recommended)

DigitalOcean provides connection pooling. Use the pooler hostname (usually port 25060):

```bash
psql "postgresql://${DO_PG_USER}:${DO_PG_PASSWORD}@${DO_PG_HOST}:25060/defaultdb?sslmode=${DO_PG_SSLMODE:-require}"
```

---

## pgAdmin Web Interface

If pgAdmin is installed and accessible:

1. Open your browser and navigate to:
   ```
   ${PGADMIN_URL}
   ```

2. Log in with:
   - Email: Your pgAdmin account email
   - Password: `${PGADMIN_MASTER_PASSWORD}`

3. Add a new server:
   - **Name**: Any descriptive name
   - **Host**: `${POSTGRES_HOST}` (local) or `${DO_PG_HOST}` (DigitalOcean)
   - **Port**: `${POSTGRES_PORT}` (local) or `${DO_PG_PORT}` (DigitalOcean)
   - **Database**: `${POSTGRES_DB}` (local) or `defaultdb` (DigitalOcean)
   - **Username**: `${POSTGRES_USER}` (local) or `${DO_PG_USER}` (DigitalOcean)
   - **Password**: Save password (stored securely in pgAdmin)

For DigitalOcean, also set:
   - **SSL Mode**: `${DO_PG_SSLMODE:-require}`

---

## Python Connection Examples

### Using psycopg2

```python
import os
import psycopg2

# Local
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

# DigitalOcean
conn = psycopg2.connect(
    host=os.getenv("DO_PG_HOST"),
    port=int(os.getenv("DO_PG_PORT", "25060")),
    database="defaultdb",
    user=os.getenv("DO_PG_USER"),
    password=os.getenv("DO_PG_PASSWORD"),
    sslmode=os.getenv("DO_PG_SSLMODE", "require"),
)
```

### Using SQLAlchemy

```python
from sqlalchemy import create_engine
import os

# Local
engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# DigitalOcean
engine = create_engine(
    f"postgresql://{os.getenv('DO_PG_USER')}:{os.getenv('DO_PG_PASSWORD')}"
    f"@{os.getenv('DO_PG_HOST')}:{os.getenv('DO_PG_PORT')}/defaultdb"
    f"?sslmode={os.getenv('DO_PG_SSLMODE', 'require')}"
)
```

---

## Environment Variables

### Local Postgres

Required:
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`

Optional (for superuser operations):
- `POSTGRES_SUPERUSER`
- `POSTGRES_SUPERUSER_PASSWORD`
- `POSTGRES_ALT_USER`
- `POSTGRES_ALT_PASSWORD`

Validate with:
```bash
make env-check-db-local
```

### DigitalOcean Postgres

Required:
- `DO_PG_HOST`
- `DO_PG_PORT`
- `DO_PG_USER`

Optional:
- `DO_PG_PASSWORD` (required for connections, but validation script doesn't check it)
- `DO_PG_SSLMODE` (default: `require`)

Validate with:
```bash
make env-check-db-do
```

---

## Security Notes

- Never commit database passwords to git
- Use connection pooling for production applications
- Enable SSL/TLS for remote database connections
- Rotate database passwords regularly
- Use least-privilege database users for applications
- Reserve superuser access for administrative tasks only

---

## Troubleshooting

### Connection Refused

- Verify host and port are correct
- Check firewall rules
- Ensure Postgres is running: `sudo systemctl status postgresql`

### Authentication Failed

- Verify username and password
- Check `pg_hba.conf` for authentication method
- Ensure user has access to the database

### SSL Errors (DigitalOcean)

- Verify `DO_PG_SSLMODE` is set correctly
- Download and use CA certificate if using `verify-full`
- Check DigitalOcean dashboard for connection details

