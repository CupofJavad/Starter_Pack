from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python .ops/scripts/convo_append.py <path_to_log.txt> <path_to_text_to_append.txt | ->")
        print("Use '-' to paste from stdin (Ctrl-D to end).")
        return 2

    log_path = Path(sys.argv[1])
    if not log_path.exists():
        print(f"Log not found: {log_path}")
        return 2

    source = sys.argv[2]
    if source == "-":
        content = sys.stdin.read()
    else:
        content = Path(source).read_text(encoding="utf-8", errors="ignore")

    stamp = f"\n\n[{datetime.now().isoformat()}] APPEND\n"
    log_path.write_text(log_path.read_text(encoding="utf-8") + stamp + content + "\n", encoding="utf-8")
    print(f"Appended to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
