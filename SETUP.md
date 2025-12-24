# Setup Guide for First-Time Users

This guide will get you from zero to ready-to-code in minutes.

## Prerequisites

- **Git** installed (check with `git --version`)
- **Python 3.8+** installed (check with `python3 --version`)
- **Make** installed (usually pre-installed on macOS/Linux)
- **Cursor IDE** (recommended but not required)

## Step 1: Clone the Repository

```bash
git clone https://github.com/CupofJavad/Starter_Pack.git
cd Starter_Pack
```

## Step 2: Bootstrap the Environment

Run the one-command setup:

```bash
make bootstrap
```

This will:
- ✅ Create a Python virtual environment (`.venv`)
- ✅ Install all dependencies
- ✅ Initialize operational directories (`.ops/`)
- ✅ Run baseline checks
- ✅ Leave you in a known-good state

**Expected output**: You should see "== Bootstrap complete ==" at the end.

## Step 3: Activate the Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt, indicating the environment is active.

**Tip**: You'll need to activate this environment every time you open a new terminal. Consider adding this to your shell profile.

## Step 4: Verify Setup

Run the smoke test to confirm everything works:

```bash
pytest tests/test_smoke.py -v
```

You should see all tests pass.

## Step 5: Open in Cursor IDE

1. Open Cursor IDE
2. File → Open Folder → Select the `Starter_Pack` directory
3. Cursor will automatically read `.cursorrules` file

## Step 6: Your First Agent Prompt

Open the Cursor chat and use the prompt from `FIRST_PROMPT.md`:

**Option 1 - Full Prompt** (Recommended for first time):
```
I just cloned this repository for the first time. Please:

1. **Verify environment setup**: Check that `make bootstrap` has been run successfully:
   - Verify .venv directory exists
   - Verify .ops directories are initialized (.ops/conversations/raw, .ops/error_kb/cases, .ops/logs)
   - If not set up, run `make bootstrap` now

2. **Read and obey all mandatory documentation** in this exact order:
   - README.md
   - .cursor/START_HERE.md
   - .cursor/PROJECT_CONTEXT.md
   - .cursor/CONTEXT_BRIEF.md
   - .cursor/ASSUMPTIONS.md
   - .cursor/BASELINE_CHECKS.md
   - .cursor/FAILURE_TO_FIX_PROTOCOL.md
   - .cursor/STOP_CONDITIONS.md
   - .cursor/PROMPT_MASTER.md
   - .cursor/PROMPT_SELF_HEALING.md
   - .cursor/CONVERSATION_POLICY.md
   - docs/anti_patterns.md
   - docs/decisions/README.md (and any existing ADRs)

3. **Confirm understanding**: After reading all files, summarize:
   - The key engineering standards I must follow
   - The workflow loop for implementing features
   - The failure handling protocol
   - The secrets/credentials policy
   - How to use the conversation vault and error KB

4. **Acknowledge**: Confirm that you will incorporate and follow all pre-defined prompts, protocols, and standards in ALL future responses. This is non-negotiable.

Once complete, I'm ready to start building. My task will be: [describe your task here]
```

**Option 2 - Quick Prompt**:
```
Read and obey: .cursor/START_HERE.md

First, verify the environment is set up (run `make bootstrap` if needed), then confirm you've read all mandatory documentation and will follow all protocols in future responses.

My task: [describe what you want to build]
```

## Troubleshooting

### `make bootstrap` fails

- **Python not found**: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- **Make not found**: 
  - macOS: Install Xcode Command Line Tools: `xcode-select --install`
  - Linux: `sudo apt-get install build-essential` (Ubuntu/Debian)
- **Permission errors**: Ensure you have write permissions in the directory

### Virtual environment not activating

- Try: `source .venv/bin/activate`
- If that doesn't work, check: `ls -la .venv/bin/activate`
- If `.venv` doesn't exist, run `make bootstrap` again

### Tests fail

- Ensure virtual environment is activated: `source .venv/bin/activate`
- Re-run bootstrap: `make bootstrap`
- Check Python version: `python3 --version` (should be 3.8+)

## Next Steps

- Read `README.md` for project overview
- Check `docs/` for detailed documentation
- Review `.cursor/START_HERE.md` to understand the agent workflow
- Start building! 🚀

## Getting Help

- Check `.ops/error_kb/` for known issues and fixes
- Review `docs/decisions/` for architectural decisions
- Consult `docs/anti_patterns.md` for common mistakes to avoid

---

**You're all set!** The repository is configured, the environment is ready, and the agent knows how to work with this codebase.

