from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(".ops/logs")


def run_capture(cmd: str) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p.returncode, p.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", required=True, help="Command to reproduce the failure")
    ap.add_argument(
        "--convo-log",
        default=None,
        help="Optional path to a raw conversation log to append to",
    )
    args = ap.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fingerprint_path = LOG_DIR / f"{ts}__env_fingerprint.txt"
    failure_path = LOG_DIR / f"{ts}__failure_output.txt"

    fp_cmd = f"{sys.executable} .ops/scripts/fingerprint_env.py"
    _, fp_out = run_capture(fp_cmd)
    fingerprint_path.write_text(fp_out, encoding="utf-8")

    code, out = run_capture(args.cmd)
    failure_path.write_text(out, encoding="utf-8")

    print(f"[diagnose] env:     {fingerprint_path}")
    print(f"[diagnose] failure: {failure_path}")
    print(f"[diagnose] exit:    {code}")

    kb_cmd = f"{sys.executable} .ops/scripts/record_failure.py {failure_path}"
    kb_code, kb_out = run_capture(kb_cmd)
    print(kb_out.strip())

    if args.convo_log:
        append_cmd = (
            f"{sys.executable} .ops/scripts/convo_append.py "
            f"{args.convo_log} {failure_path}"
        )
        a_code, a_out = run_capture(append_cmd)
        print(a_out.strip())
        if a_code != 0:
            print("[diagnose] WARNING: failed to append to convo log")

    return 0 if kb_code == 0 else kb_code


if __name__ == "__main__":
    raise SystemExit(main())
