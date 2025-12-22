# Starter Pack Finalization Checklist

Use this checklist to verify everything is ready for future use.

---

## ✅ Pre-Flight Checks

- [ ] `.env` file exists with your actual secrets
- [ ] `.env` is NOT tracked by git (`git status` shows no `.env`)
- [ ] `.env.example` has all variables (with blank/placeholder values)
- [ ] `.gitignore` includes `.env`

---

## ✅ Testing (Run with venv activated)

### Basic Functionality

```bash
. .venv/bin/activate

# 1. Settings loads without secrets
python -c "from app.settings import Settings; s = Settings.load(); print('✓ Settings works')"

# 2. All tests pass
pytest tests/ -v

# 3. Code quality
ruff check .
pyright
```

### Environment Validation

```bash
# Test each mode (will fail if vars not set - that's OK for testing)
make env-check-local-dev
make env-check-server-ops  
make env-check-db-local
make env-check-db-do
```

### With Your Actual Secrets

```bash
# Quick test that your secrets load (create temp file, don't commit)
cat > /tmp/test_my_secrets.py << 'EOF'
import os
os.environ.setdefault('APP_ENV', 'dev')
os.environ.setdefault('LOG_LEVEL', 'INFO')
# Load your .env if using python-dotenv or similar
from app.settings import Settings
s = Settings.load()
print(f"✓ Loaded {len([v for v in dir(s) if not v.startswith('_')])} settings")
print(f"✓ HF_TOKEN set: {s.hf_token is not None}")
print(f"✓ GITHUB_TOKEN set: {s.github_token is not None}")
EOF

python /tmp/test_my_secrets.py
rm /tmp/test_my_secrets.py
```

---

## ✅ Documentation Review

- [ ] `docs/env-vars.md` - Complete and accurate
- [ ] `docs/server-access.md` - SSH examples work
- [ ] `docs/db-access.md` - Connection examples work
- [ ] `docs/TESTING_GUIDE.md` - Testing instructions clear
- [ ] `README.md` - Updated with new sections
- [ ] `.cursor/PROJECT_CONTEXT.md` - Updated tool list

---

## ✅ Security Verification

- [ ] No secrets in git: `git grep -i "password\|token\|secret" -- "*.py" "*.md" | grep -v "REDACTED\|example\|placeholder"` should show no actual values
- [ ] Logging redaction works: All secrets in `REDACT_KEYS` are redacted
- [ ] Settings.load() doesn't crash without secrets
- [ ] Tests don't require secrets to pass

---

## ✅ Fresh Clone Test

Simulate a new user cloning the repo:

```bash
# In a different directory
cd /tmp
rm -rf test-starter-clone
git clone <your-repo-url> test-starter-clone
cd test-starter-clone

# Should work without .env
make bootstrap
. .venv/bin/activate
pytest tests/test_smoke.py -v  # Should pass

# Settings should work
python -c "from app.settings import Settings; s = Settings.load(); print('✓ Works')"

# Cleanup
cd ~
rm -rf /tmp/test-starter-clone
```

---

## ✅ Final Git Status

```bash
# Review what will be committed
git status

# Verify .env is NOT in the list
git status | grep -E "\.env$" && echo "⚠ WARNING: .env is tracked!" || echo "✓ .env not tracked"

# Review changes
git diff --cached
```

---

## ✅ Commit and Push

Once all checks pass:

```bash
# Add new files
git add tests/ docs/TESTING_GUIDE.md docs/FINALIZATION_CHECKLIST.md

# Review
git status

# Commit
git commit -m "test: add comprehensive test suite and finalization docs"

# Push
git push
```

---

## 🎯 Ready for Use

Once finalized, the starter pack is ready for:

1. **Cloning for new projects:**
   ```bash
   git clone <your-repo-url> my-new-project
   cd my-new-project
   cp .env.example .env
   # Edit .env with project-specific values
   make bootstrap
   ```

2. **Sharing with team:**
   - All secrets stay local (in `.env`)
   - Documentation guides setup
   - Tests verify functionality

3. **Future updates:**
   - Pull latest changes
   - Merge any new env vars into your `.env`
   - Run tests to verify compatibility

---

## 📝 Quick Reference

**Test everything:**
```bash
make bootstrap && . .venv/bin/activate && pytest tests/ -v && ruff check . && pyright
```

**Check env vars:**
```bash
make env-check-local-dev
make env-check-server-ops
make env-check-db-local
make env-check-db-do
```

**Verify security:**
```bash
git status | grep "\.env" || echo "✓ .env not tracked"
```

---

## 🚨 If Something Fails

1. **Tests fail:** Check `docs/TESTING_GUIDE.md` for troubleshooting
2. **Env validation fails:** Expected if vars not set - set them in `.env` to test
3. **Type errors:** Run `pyright` for details, fix type hints
4. **Lint errors:** Run `ruff check .` and fix issues

---

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

