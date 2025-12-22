from __future__ import annotations

import logging
import os

REDACT_KEYS = {"HF_TOKEN", "NAMESILO_API_KEY"}


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
