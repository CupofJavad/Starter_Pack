from __future__ import annotations

import json
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


class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter (timestamp, level, logger, lineno, message)."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "lineno": record.lineno,
            "message": record.getMessage(),
        }
        return json.dumps(log, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging with secret redaction.

    By default, logs are human-readable text. If the environment variable
    STRUCTURED_LOGGING is set to a truthy value (\"1\", \"true\", \"yes\", \"json\"),
    logs are emitted as JSON objects suitable for log aggregation systems.
    """
    structured_flag = os.getenv("STRUCTURED_LOGGING", "").strip().lower()
    use_structured = structured_flag in {"1", "true", "yes", "json"}

    if use_structured:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        handlers = [handler]
        fmt = None
    else:
        handlers = None
        fmt = "%(asctime)s %(levelname)s %(name)s:%(lineno)d - %(message)s"

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=fmt,
        handlers=handlers,
    )

    logging.getLogger().addFilter(RedactingFilter())
