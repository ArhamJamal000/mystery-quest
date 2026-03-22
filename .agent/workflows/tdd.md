---
description: Enforce test-driven development (RED → GREEN → REFACTOR) for any feature or bugfix
---

# /tdd — Test-Driven Development Workflow

Always follow the RED → GREEN → REFACTOR cycle. Never write implementation before tests.

## Steps

1. **RED — Write a failing test**
   - Define the interface/function signature first (no implementation)
   - Write a test that describes the expected behaviour
   - Run the test — confirm it FAILS with the right error (not a syntax error)
   - Show the failing test output to the user

2. **GREEN — Write minimal implementation**
   - Write the smallest code that makes the test pass
   - Do NOT over-engineer at this stage
   - Run the test — confirm it PASSES
   - Show the passing test output

3. **REFACTOR — Improve the code**
   - Clean up duplication, naming, structure
   - Ensure tests still pass after refactor
   - Aim for 80%+ coverage on the changed code

4. **Verify coverage**
   - Run the full test suite (not just the new test)
   - Report: tests added, tests passing, coverage % (if measurable)

## Rules
- If fixing a bug: write a failing test that **reproduces the bug first**, then fix
- Never skip RED — always see the test fail before it passes
- Commit after GREEN, before REFACTOR
