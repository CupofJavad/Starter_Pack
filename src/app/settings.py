from __future__ import annotations

from dataclasses import dataclass
import os


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
    app_env: str
    log_level: str
    hf_token: str | None
    namesilo_api_key: str | None

    @staticmethod
    def load() -> "Settings":
        return Settings(
            app_env=os.getenv("APP_ENV", "dev"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            hf_token=os.getenv("HF_TOKEN"),
            namesilo_api_key=os.getenv("NAMESILO_API_KEY"),
        )

    def require_hf_token(self) -> str:
        return self.hf_token or _require_env("HF_TOKEN")

    def require_namesilo_key(self) -> str:
        return self.namesilo_api_key or _require_env("NAMESILO_API_KEY")
