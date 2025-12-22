from __future__ import annotations

from pathlib import Path
import re
import sys
from datetime import datetime

BRIEF_DIR = Path(".ops/conversations/briefs")


def redact(text: str) -> str:
    text = re.sub(r"(HF_TOKEN\s*=\s*)(\S+)", r"\1[REDACTED]", text)
    text = re.sub(r"(NAMESILO_API_KEY\s*=\s*)(\S+)", r"\1[REDACTED]", text)
    text = re.sub(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*\S+", r"\1: [REDACTED]", text)
    return text


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python .ops/scripts/convo_brief.py <path_to_raw_log.txt>")
        return 2

    raw_path = Path(sys.argv[1])
    if not raw_path.exists():
        print(f"Not found: {raw_path}")
        return 2

    BRIEF_DIR.mkdir(parents=True, exist_ok=True)

    raw = raw_path.read_text(encoding="utf-8", errors="ignore")
    raw = redact(raw)

    brief = f"""# Conversation Brief
Source: {raw_path}
Generated: {datetime.now().isoformat()}

## What we were trying to do
- (fill in)

## What we decided
- (fill in)

## What changed / what we built
- (fill in)

## Open issues / blockers
- (fill in)

## Next steps
1)
2)
3)

## Raw excerpt (redacted)
```text
{raw[-4000:]}
```
"""

    out = BRIEF_DIR / f"{raw_path.stem}__brief.md"
    out.write_text(brief, encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
