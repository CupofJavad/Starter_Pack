#!/usr/bin/env python3
"""Verify that the repository is properly set up for first-time users."""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent


def check_virtual_env() -> tuple[bool, str]:
    """Check if virtual environment exists and is activated."""
    venv_path = REPO_ROOT / ".venv"
    if not venv_path.exists():
        return False, "Virtual environment (.venv) not found. Run: make bootstrap"
    
    activate_script = venv_path / "bin" / "activate"
    if not activate_script.exists():
        return False, "Virtual environment appears incomplete. Run: make bootstrap"
    
    # Check if activated (not perfect, but helpful)
    if os.environ.get("VIRTUAL_ENV") is None:
        return True, "Virtual environment exists but not activated. Run: source .venv/bin/activate"
    
    return True, "Virtual environment exists and appears activated"


def check_ops_directories() -> tuple[bool, str]:
    """Check if .ops directories are initialized."""
    required_dirs = [
        ".ops/conversations/raw",
        ".ops/conversations/briefs",
        ".ops/error_kb/cases",
        ".ops/logs",
    ]
    
    missing = []
    for dir_path in required_dirs:
        full_path = REPO_ROOT / dir_path
        if not full_path.exists():
            missing.append(dir_path)
    
    if missing:
        return False, f"Missing directories: {', '.join(missing)}. Run: make bootstrap"
    
    return True, "All .ops directories exist"


def check_dependencies() -> tuple[bool, str]:
    """Check if key dependencies are installed."""
    try:
        import pytest
        import ruff
        # Try to import pyright (it's a CLI tool, so we check if it's callable)
        import subprocess
        result = subprocess.run(
            ["pyright", "--version"],
            capture_output=True,
            timeout=5,
        )
        pyright_available = result.returncode == 0
    except ImportError as e:
        return False, f"Dependencies not installed: {e}. Run: make bootstrap"
    except Exception:
        pyright_available = False
    
    if not pyright_available:
        return True, "Dependencies installed (pyright may need separate install)"
    
    return True, "Key dependencies are installed"


def check_cursor_files() -> tuple[bool, str]:
    """Check if key Cursor configuration files exist."""
    required_files = [
        ".cursorrules",
        ".cursor/START_HERE.md",
        "FIRST_PROMPT.md",
        "SETUP.md",
    ]
    
    missing = []
    for file_path in required_files:
        full_path = REPO_ROOT / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    
    return True, "All Cursor configuration files exist"


def main() -> int:
    """Run all setup verification checks."""
    print("🔍 Verifying repository setup...\n")
    
    checks = [
        ("Virtual Environment", check_virtual_env),
        (".ops Directories", check_ops_directories),
        ("Dependencies", check_dependencies),
        ("Cursor Files", check_cursor_files),
    ]
    
    all_passed = True
    for name, check_func in checks:
        passed, message = check_func()
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {message}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ Setup verification complete! You're ready to go.")
        print("\nNext steps:")
        print("1. Open this folder in Cursor IDE")
        print("2. Use the prompt from FIRST_PROMPT.md in your first Cursor chat")
        return 0
    else:
        print("❌ Setup incomplete. Please address the issues above.")
        print("\nQuick fix: Run 'make bootstrap' to set up the environment.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

