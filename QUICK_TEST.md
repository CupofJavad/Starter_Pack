# Quick Test Instructions

## If tests fail with "ModuleNotFoundError: No module named 'app'"

**Solution:** Activate the virtual environment first:

```bash
# Activate venv
. .venv/bin/activate

# Then run tests
pytest tests/ -v
```

## If venv doesn't exist

```bash
# Bootstrap the environment
make bootstrap

# Then activate and test
. .venv/bin/activate
pytest tests/ -v
```

## Quick verification

```bash
# 1. Check if venv exists
test -d .venv && echo "✓ venv exists" || echo "⚠ Run: make bootstrap"

# 2. Activate venv
. .venv/bin/activate

# 3. Run tests
pytest tests/ -v
```

The `conftest.py` file automatically adds `src/` to the Python path, so imports should work once the venv is activated.
