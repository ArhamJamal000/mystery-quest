---
description: Debug any issue methodically — reproduce, isolate, fix, and verify
---

# /debug — Debugging Workflow

## Usage
`/debug <description of the issue>` — start a structured debug session

## Steps

1. **Reproduce the issue**
   - State exact steps to reproduce
   - Identify what the expected vs actual behaviour is
   - Note: OS, version, environment (dev/prod?)

2. **Gather evidence**
   - Read relevant error logs / stack traces
   - Add temporary logging if needed to isolate the problem
   - Check recent git changes that may have introduced the bug

3. **Form hypotheses (max 3)**
   - List the most likely causes ranked by probability
   - For each: explain reasoning

4. **Test hypotheses — cheapest/fastest first**
   - Verify each hypothesis by checking code or adding a test
   - Eliminate hypotheses one by one

5. **Fix**
   - Apply the minimal fix for the root cause
   - Write a failing test that caught the bug (if possible)
   - Verify the fix resolves the issue

6. **Post-mortem (optional)**
   - Why did this bug occur?
   - How can it be prevented in future?

> [!TIP]
> If you're stuck after 3 hypotheses, step back and question your assumptions about what the code *should* do.
