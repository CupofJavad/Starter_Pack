from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_check_env_local_dev_success():
    """check_env.py should pass when required vars are set."""
    script = Path(".ops/scripts/check_env.py")
    assert script.exists(), "check_env.py not found"
    
    # Set required vars
    os.environ["APP_ENV"] = "dev"
    os.environ["LOG_LEVEL"] = "INFO"
    
    result = subprocess.run(
        [sys.executable, str(script), "local-dev"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "✓" in result.stdout or "present" in result.stdout.lower()
    
    # Cleanup
    del os.environ["APP_ENV"]
    del os.environ["LOG_LEVEL"]


def test_check_env_local_dev_failure():
    """check_env.py should fail when required vars are missing."""
    script = Path(".ops/scripts/check_env.py")
    
    # Clear required vars
    for key in ["APP_ENV", "LOG_LEVEL"]:
        if key in os.environ:
            del os.environ[key]
    
    result = subprocess.run(
        [sys.executable, str(script), "local-dev"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 2, "Should exit with code 2 on failure"
    assert "Missing" in result.stderr or "missing" in result.stderr.lower()


def test_check_env_invalid_mode():
    """check_env.py should fail with invalid mode."""
    script = Path(".ops/scripts/check_env.py")
    
    result = subprocess.run(
        [sys.executable, str(script), "invalid-mode"],
        capture_output=True,
        text=True,
    )
    
    assert result.returncode == 2
    assert "Unknown mode" in result.stderr or "invalid" in result.stderr.lower()

