from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sys

ROOT = Path(".ops/conversations/raw")


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "conversation"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python .ops/scripts/convo_new.py <topic/title>")
        return 2

    title = " ".join(sys.argv[1:])
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{ts}__{slugify(title)}.txt"

    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / fname

    header = (
        f"TITLE: {title}\n"
        f"CREATED: {datetime.now().isoformat()}\n"
        "FORMAT: raw_text\n"
        "\n"
        "---- BEGIN LOG ----\n\n"
    )
    path.write_text(header, encoding="utf-8")
    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
