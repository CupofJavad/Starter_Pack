# Your First Cursor Prompt (Copy & Paste)

After cloning this repository and running `make bootstrap`, use this prompt in Cursor:

---

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

---

## Quick Version (If you prefer shorter)

```
Read and obey: .cursor/START_HERE.md

First, verify the environment is set up (run `make bootstrap` if needed), then confirm you've read all mandatory documentation and will follow all protocols in future responses.

My task: [describe what you want to build]
```

---

**Note**: The `.cursorrules` file in this repo will automatically be read by Cursor, but explicitly referencing `.cursor/START_HERE.md` ensures all documentation is loaded.

