from __future__ import annotations

import os

import pytest

from app.settings import Settings


def test_settings_loads_without_secrets():
    """Settings.load() should work even when no secrets are set."""
    s = Settings.load()
    assert s.app_env == "dev"  # default
    assert s.log_level == "INFO"  # default
    # All optional fields should be None when not set
    assert s.hf_token is None
    assert s.github_token is None
    assert s.postgres_password is None


def test_settings_parses_integers():
    """Port fields should parse as integers or None."""
    # Test with no port set
    s = Settings.load()
    assert s.postgres_port is None or isinstance(s.postgres_port, int)
    assert s.lunaverse_ssh_port is None or isinstance(s.lunaverse_ssh_port, int)
    assert s.do_pg_port is None or isinstance(s.do_pg_port, int)

    # Test with valid port
    os.environ["POSTGRES_PORT"] = "5432"
    s = Settings.load()
    assert s.postgres_port == 5432
    del os.environ["POSTGRES_PORT"]

    # Test with invalid port (should be None)
    os.environ["POSTGRES_PORT"] = "not-a-number"
    s = Settings.load()
    assert s.postgres_port is None
    del os.environ["POSTGRES_PORT"]


def test_require_methods_raise_when_missing():
    """require_* methods should raise RuntimeError when env var is missing."""
    s = Settings.load()
    
    # Clear any existing env vars
    for key in ["HF_TOKEN", "GITHUB_TOKEN", "POSTGRES_PASSWORD"]:
        if key in os.environ:
            del os.environ[key]
    
    s = Settings.load()
    
    with pytest.raises(RuntimeError, match="Missing required environment variable"):
        s.require_hf_token()
    
    with pytest.raises(RuntimeError, match="Missing required environment variable"):
        s.require_github_token()
    
    with pytest.raises(RuntimeError, match="Missing required environment variable"):
        s.require_postgres_password()


def test_require_methods_return_value_when_set():
    """require_* methods should return the value when set."""
    os.environ["HF_TOKEN"] = "test_token_123"
    os.environ["GITHUB_TOKEN"] = "gh_test_token"
    
    s = Settings.load()
    assert s.require_hf_token() == "test_token_123"
    assert s.require_github_token() == "gh_test_token"
    
    # Cleanup
    del os.environ["HF_TOKEN"]
    del os.environ["GITHUB_TOKEN"]


def test_settings_all_fields_accessible():
    """All new fields should be accessible (even if None)."""
    s = Settings.load()
    
    # Server config
    assert hasattr(s, "server_admin_name")
    assert hasattr(s, "server_name")
    
    # Lunaverse
    assert hasattr(s, "lunaverse_host")
    assert hasattr(s, "lunaverse_ssh_user")
    assert hasattr(s, "lunaverse_ssh_port")
    
    # Cockpit & pgAdmin
    assert hasattr(s, "cockpit_url")
    assert hasattr(s, "pgadmin_url")
    
    # Postgres
    assert hasattr(s, "postgres_host")
    assert hasattr(s, "postgres_user")
    
    # DigitalOcean
    assert hasattr(s, "do_pg_host")
    assert hasattr(s, "do_pg_user")
    
    # Tokens
    assert hasattr(s, "taskade_token")
    assert hasattr(s, "hf_ssh_key_fingerprint")
    
    # NameSilo
    assert hasattr(s, "namesilo_account_url")
    assert hasattr(s, "namesilo_site_builder_url")

