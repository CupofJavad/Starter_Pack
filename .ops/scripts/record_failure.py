import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

KB_DIR = Path(".ops/error_kb")
CASES_DIR = KB_DIR / "cases"
INDEX = KB_DIR / "error_index.json"


def signature_from_text(text: str) -> str:
    norm = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python .ops/scripts/record_failure.py <path_to_error_log.txt>")
        return 2

    error_text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
    sig = signature_from_text(error_text)

    case_dir = CASES_DIR / sig
    case_dir.mkdir(parents=True, exist_ok=True)

    (case_dir / "symptoms.md").write_text(
        f"# Symptoms\n\nCaptured: {datetime.utcnow().isoformat()}Z\n\n```\n{error_text}\n```\n",
        encoding="utf-8",
    )
    (case_dir / "root_cause.md").write_text("# Root Cause\n\nTBD\n", encoding="utf-8")
    (case_dir / "fix.md").write_text("# Fix\n\nTBD\n", encoding="utf-8")
    (case_dir / "regression_test.md").write_text("# Regression Test\n\nTBD\n", encoding="utf-8")

    index = {}
    if INDEX.exists():
        index = json.loads(INDEX.read_text(encoding="utf-8"))
    index.setdefault(sig, {"cases": []})
    if str(case_dir) not in index[sig]["cases"]:
        index[sig]["cases"].append(str(case_dir))

    INDEX.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Recorded failure signature: {sig} -> {case_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
