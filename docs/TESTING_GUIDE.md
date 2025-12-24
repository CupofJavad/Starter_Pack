# Testing and Finalization Guide

This guide walks through testing and finalizing the starter pack for future use.

---

## Prerequisites

1. **Your `.env` file is populated** with actual secrets (not committed to git)
2. **Python 3.11+** is available
3. **Virtual environment** is set up (via `make bootstrap`)
4. **Virtual environment is activated** before running tests

---

## Step 1: Bootstrap and Environment Setup

```bash
# If not already done, bootstrap the environment
make bootstrap

# Activate the virtual environment (REQUIRED before running tests)
. .venv/bin/activate
# OR
source .venv/bin/activate

# Verify activation (should show .venv path)
which python
```

**Important:** If you see `ModuleNotFoundError: No module named 'app'`, you need to:
1. Activate the venv: `. .venv/bin/activate`
2. Or ensure the package is installed: `pip install -e .`

---

## Step 2: Run Test Suite

### Basic Smoke Test

```bash
pytest tests/test_smoke.py -v
```

Expected: ✓ Passes (Settings.load() works without secrets)

### Settings Tests

```bash
pytest tests/test_settings.py -v
```

Tests:
- ✓ Settings loads without secrets
- ✓ Integer parsing for ports
- ✓ require_* methods raise when missing
- ✓ require_* methods return values when set
- ✓ All new fields are accessible

### Logging Redaction Tests

```bash
pytest tests/test_logging_redaction.py -v
```

Tests:
- ✓ Secrets are redacted from log messages
- ✓ All REDACT_KEYS are redacted
- ✓ Partial matches work correctly
- ✓ No false positives

### Environment Validation Tests

```bash
pytest tests/test_check_env.py -v
```

Tests:
- ✓ check_env.py validates correctly
- ✓ Fails when vars are missing
- ✓ Handles invalid modes

### Full Test Suite

```bash
pytest tests/ -v
```

All tests should pass.

---

## Step 3: Test Environment Validation Script

Test each validation mode:

```bash
# Local development (should pass if APP_ENV and LOG_LEVEL are set)
make env-check-local-dev

# Server operations (requires LUNAVERSE_* vars)
make env-check-server-ops

# Local Postgres (requires POSTGRES_* vars)
make env-check-db-local

# DigitalOcean Postgres (requires DO_PG_* vars)
make env-check-db-do
```

**Note:** These will fail if the required env vars aren't set in your `.env` file. That's expected - the script is working correctly.

---

## Step 4: Test Settings with Your Actual Secrets

Create a quick test script to verify Settings loads your actual values:

```python
# test_my_env.py (temporary, don't commit)
from app.settings import Settings

s = Settings.load()

# Test that your secrets are loaded (values won't print, but you can check they exist)
print(f"✓ APP_ENV: {s.app_env}")
print(f"✓ LOG_LEVEL: {s.log_level}")
print(f"✓ HF_TOKEN set: {s.hf_token is not None}")
print(f"✓ GITHUB_TOKEN set: {s.github_token is not None}")
print(f"✓ POSTGRES_HOST: {s.postgres_host}")
print(f"✓ LUNAVERSE_HOST: {s.lunaverse_host}")

# Test require methods (these will raise if secrets are missing)
try:
    if s.hf_token:
        token = s.require_hf_token()
        print(f"✓ require_hf_token() works")
except RuntimeError as e:
    print(f"⚠ HF_TOKEN not set: {e}")
```

Run it:
```bash
python test_my_env.py
```

**Important:** Delete `test_my_env.py` after testing - never commit it.

---

## Step 5: Test Logging Redaction

Verify secrets are redacted in logs:

```python
# test_logging.py (temporary)
import logging
from app.logging_config import configure_logging

configure_logging("DEBUG")
logger = logging.getLogger("test")

# This should be redacted if HF_TOKEN is set
logger.info(f"Connecting with token {os.getenv('HF_TOKEN', 'not_set')}")
```

Check the output - secrets should appear as `[REDACTED]`.

---

## Step 6: Code Quality Checks

```bash
# Linting
ruff check .

# Type checking
pyright

# Format check
ruff format --check .
```

All should pass.

### Optional: One-Command Quality Gate

For a quick **industry-standard quality gate** that matches what you would run in CI,
use the bundled `make` target:

```bash
make quality
```

This runs, in order:
- `ruff check .`
- `pyright`
- `pytest tests/ -q`

Use this before commits or releases to ensure the repo is in a healthy state.

---

## Step 7: Verify Documentation

Check that all documentation is accessible and accurate:

```bash
# Read through these files
cat docs/env-vars.md
cat docs/server-access.md
cat docs/db-access.md

# Verify .env.example has all variables
cat .env.example
```

---

## Step 8: Test Fresh Clone Scenario

Simulate what happens when someone clones this repo:

```bash
# In a temporary directory
cd /tmp
git clone <your-repo-url> test-starter-pack
cd test-starter-pack

# Should work without .env file
make bootstrap
. .venv/bin/activate
pytest tests/test_smoke.py -v  # Should pass

# Settings should load without secrets
python -c "from app.settings import Settings; s = Settings.load(); print('✓ Works without secrets')"
```

---

## Step 9: Final Verification Checklist

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Linting passes: `ruff check .`
- [ ] Type checking passes: `pyright`
- [ ] `.env` is not tracked: `git status` shows no `.env`
- [ ] `.env.example` has all variables (with blank values)
- [ ] Documentation is complete and accurate
- [ ] Settings.load() works without secrets
- [ ] Logging redaction works for all secrets
- [ ] Environment validation script works for all modes
- [ ] Fresh clone scenario works (tested in Step 8)

---

## Step 10: Commit and Push

Once everything passes:

```bash
# Review changes
git status
git diff

# Add all new files
git add tests/ docs/TESTING_GUIDE.md

# Commit
git commit -m "test: add comprehensive test suite and testing guide"

# Push
git push
```

---

## Common Issues and Solutions

### Issue: Tests fail because secrets are missing

**Solution:** Tests are designed to work WITHOUT secrets. If a test requires secrets, it's a bug. Tests should only verify that:
- Settings.load() works without secrets
- require_* methods raise when secrets are missing
- Logging redaction works

### Issue: Environment validation fails

**Solution:** This is expected if you haven't set the required env vars. The validation script is working correctly. Set the vars in your `.env` file to test the success path.

### Issue: Type checking errors

**Solution:** Run `pyright` to see specific errors. Common issues:
- Missing type hints
- Incorrect return types
- Import errors

### Issue: .env is tracked by git

**Solution:** 
```bash
# Remove from git (but keep file)
git rm --cached .env

# Verify .gitignore has .env
grep "^\.env$" .gitignore
```

---

## Next Steps After Finalization

1. **Tag a release:**
   ```bash
   git tag -a v1.0.0 -m "Initial starter pack release"
   git push --tags
   ```

2. **Update README** with any project-specific notes

3. **Clone and test** in a new directory to simulate real usage

4. **Document any project-specific setup** in CONTEXT_BRIEF.md

---

## Security Reminders

- ✅ Never commit `.env` file
- ✅ Never print secret values in tests
- ✅ Always redact secrets in logs
- ✅ Use `require_*` methods only when secrets are actually needed
- ✅ Tests should work without secrets

