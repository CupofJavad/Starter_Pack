from __future__ import annotations

import logging
import os

REDACT_KEYS = {
    "LUNAVERSE_SSH_PASSWORD",
    "POSTGRES_PASSWORD",
    "POSTGRES_SUPERUSER_PASSWORD",
    "POSTGRES_ALT_PASSWORD",
    "PGADMIN_MASTER_PASSWORD",
    "DEFAULT_ADMIN_PASSWORD",
    "LUNAVERSE_APP_PASSWORD",
    "HF_TOKEN",
    "GITHUB_TOKEN",
    "TASKADE_TOKEN",
    "NAMESILO_API_KEY",
    "DO_PG_PASSWORD",
}


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for k in REDACT_KEYS:
            v = os.getenv(k)
            if v and v in msg:
                record.msg = msg.replace(v, "[REDACTED]")
        return True


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s:%(lineno)d - %(message)s",
    )
    logging.getLogger().addFilter(RedactingFilter())
