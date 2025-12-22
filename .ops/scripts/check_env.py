from __future__ import annotations

import argparse
import os
import sys

MODES = {
    "local-dev": {
        "required": [
            "APP_ENV",
            "LOG_LEVEL",
        ],
        "description": "Local development environment",
    },
    "server-ops": {
        "required": [
            "LUNAVERSE_HOST",
            "LUNAVERSE_SSH_USER",
            "LUNAVERSE_SSH_PORT",
        ],
        "description": "Server operations (SSH access to Lunaverse)",
    },
    "db-local": {
        "required": [
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_DB",
            "POSTGRES_USER",
        ],
        "description": "Local Postgres database access",
    },
    "db-do": {
        "required": [
            "DO_PG_HOST",
            "DO_PG_PORT",
            "DO_PG_USER",
        ],
        "description": "DigitalOcean Postgres database access",
    },
}


def check_mode(mode: str) -> int:
    if mode not in MODES:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        print(f"Available modes: {', '.join(MODES.keys())}", file=sys.stderr)
        return 2

    config = MODES[mode]
    missing = []

    for var_name in config["required"]:
        value = os.getenv(var_name, "").strip()
        if not value:
            missing.append(var_name)

    if missing:
        print(f"Missing required environment variables for mode '{mode}':", file=sys.stderr)
        for var_name in missing:
            print(f"  - {var_name}", file=sys.stderr)
        return 2

    print(f"✓ All required environment variables present for mode '{mode}'")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check that required environment variables are set for a given mode"
    )
    ap.add_argument(
        "mode",
        choices=list(MODES.keys()),
        help=f"Mode to check: {', '.join(MODES.keys())}",
    )
    args = ap.parse_args()
    return check_mode(args.mode)


if __name__ == "__main__":
    raise SystemExit(main())

