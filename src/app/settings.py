from __future__ import annotations

import os
from dataclasses import dataclass


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Set it in your local .env (gitignored) or your shell environment."
        )
    return value


@dataclass(frozen=True)
class Settings:
    # App config
    app_env: str
    log_level: str

    # Server config
    server_admin_name: str | None
    server_name: str | None

    # Lunaverse SSH
    lunaverse_host: str | None
    lunaverse_ssh_user: str | None
    lunaverse_ssh_port: int | None
    lunaverse_ssh_password: str | None
    lunaverse_ssh_tailscale_host: str | None

    # Cockpit & pgAdmin
    cockpit_url: str | None
    pgadmin_url: str | None
    pgadmin_master_password: str | None

    # Local Postgres
    postgres_host: str | None
    postgres_port: int | None
    postgres_db: str | None
    postgres_user: str | None
    postgres_password: str | None
    postgres_superuser: str | None
    postgres_superuser_password: str | None
    postgres_alt_user: str | None
    postgres_alt_password: str | None

    # Default admin
    default_admin_email: str | None
    default_admin_password: str | None
    default_admin_role: str | None

    # App user
    lunaverse_app_user: str | None
    lunaverse_app_password: str | None

    # API tokens
    github_token: str | None
    hf_token: str | None
    hf_ssh_key_fingerprint: str | None

    # DigitalOcean Postgres
    do_pg_host: str | None
    do_pg_port: int | None
    do_pg_user: str | None
    do_pg_password: str | None
    do_pg_sslmode: str | None

    # Taskade
    taskade_token: str | None

    # NameSilo
    namesilo_api_key: str | None
    namesilo_account_url: str | None
    namesilo_site_builder_url: str | None

    @staticmethod
    def _parse_int(value: str | None) -> int | None:
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def load() -> Settings:
        return Settings(
            app_env=os.getenv("APP_ENV", "dev"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            server_admin_name=os.getenv("SERVER_ADMIN_NAME"),
            server_name=os.getenv("SERVER_NAME"),
            lunaverse_host=os.getenv("LUNAVERSE_HOST"),
            lunaverse_ssh_user=os.getenv("LUNAVERSE_SSH_USER"),
            lunaverse_ssh_port=Settings._parse_int(os.getenv("LUNAVERSE_SSH_PORT")),
            lunaverse_ssh_password=os.getenv("LUNAVERSE_SSH_PASSWORD"),
            lunaverse_ssh_tailscale_host=os.getenv("LUNAVERSE_SSH_TAILSCALE_HOST"),
            cockpit_url=os.getenv("COCKPIT_URL"),
            pgadmin_url=os.getenv("PGADMIN_URL"),
            pgadmin_master_password=os.getenv("PGADMIN_MASTER_PASSWORD"),
            postgres_host=os.getenv("POSTGRES_HOST"),
            postgres_port=Settings._parse_int(os.getenv("POSTGRES_PORT")),
            postgres_db=os.getenv("POSTGRES_DB"),
            postgres_user=os.getenv("POSTGRES_USER"),
            postgres_password=os.getenv("POSTGRES_PASSWORD"),
            postgres_superuser=os.getenv("POSTGRES_SUPERUSER"),
            postgres_superuser_password=os.getenv("POSTGRES_SUPERUSER_PASSWORD"),
            postgres_alt_user=os.getenv("POSTGRES_ALT_USER"),
            postgres_alt_password=os.getenv("POSTGRES_ALT_PASSWORD"),
            default_admin_email=os.getenv("DEFAULT_ADMIN_EMAIL"),
            default_admin_password=os.getenv("DEFAULT_ADMIN_PASSWORD"),
            default_admin_role=os.getenv("DEFAULT_ADMIN_ROLE"),
            lunaverse_app_user=os.getenv("LUNAVERSE_APP_USER"),
            lunaverse_app_password=os.getenv("LUNAVERSE_APP_PASSWORD"),
            github_token=os.getenv("GITHUB_TOKEN"),
            hf_token=os.getenv("HF_TOKEN"),
            hf_ssh_key_fingerprint=os.getenv("HF_SSH_KEY_FINGERPRINT"),
            do_pg_host=os.getenv("DO_PG_HOST"),
            do_pg_port=Settings._parse_int(os.getenv("DO_PG_PORT")),
            do_pg_user=os.getenv("DO_PG_USER"),
            do_pg_password=os.getenv("DO_PG_PASSWORD"),
            do_pg_sslmode=os.getenv("DO_PG_SSLMODE"),
            taskade_token=os.getenv("TASKADE_TOKEN"),
            namesilo_api_key=os.getenv("NAMESILO_API_KEY"),
            namesilo_account_url=os.getenv("NAMESILO_ACCOUNT_URL"),
            namesilo_site_builder_url=os.getenv("NAMESILO_SITE_BUILDER_URL"),
        )

    # Require methods for secrets
    def require_hf_token(self) -> str:
        return self.hf_token or _require_env("HF_TOKEN")

    def require_namesilo_key(self) -> str:
        return self.namesilo_api_key or _require_env("NAMESILO_API_KEY")

    def require_github_token(self) -> str:
        return self.github_token or _require_env("GITHUB_TOKEN")

    def require_taskade_token(self) -> str:
        return self.taskade_token or _require_env("TASKADE_TOKEN")

    def require_lunaverse_ssh_password(self) -> str:
        return self.lunaverse_ssh_password or _require_env("LUNAVERSE_SSH_PASSWORD")

    def require_postgres_password(self) -> str:
        return self.postgres_password or _require_env("POSTGRES_PASSWORD")

    def require_postgres_superuser_password(self) -> str:
        return self.postgres_superuser_password or _require_env("POSTGRES_SUPERUSER_PASSWORD")

    def require_postgres_alt_password(self) -> str:
        return self.postgres_alt_password or _require_env("POSTGRES_ALT_PASSWORD")

    def require_pgadmin_master_password(self) -> str:
        return self.pgadmin_master_password or _require_env("PGADMIN_MASTER_PASSWORD")

    def require_default_admin_password(self) -> str:
        return self.default_admin_password or _require_env("DEFAULT_ADMIN_PASSWORD")

    def require_lunaverse_app_password(self) -> str:
        return self.lunaverse_app_password or _require_env("LUNAVERSE_APP_PASSWORD")

    def require_do_pg_password(self) -> str:
        return self.do_pg_password or _require_env("DO_PG_PASSWORD")
