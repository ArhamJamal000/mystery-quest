---
description: Refactor code for clarity, maintainability, and performance without changing behaviour
---

# /refactor — Refactor Workflow

Safely improve code structure without changing external behaviour.

## Usage
`/refactor <file or function>` — refactor a specific target  
`/refactor` — identify and refactor the worst code smells in the active file

## Steps

1. **Identify code smells**
   - Long functions (>40 lines)
   - Deep nesting (>3 levels)
   - Duplicated logic (DRY violations)
   - Magic numbers or strings (extract to constants)
   - Poorly named variables/functions
   - God objects or classes doing too much

2. **Write/run tests BEFORE refactoring** (or confirm existing tests cover the target)

3. **Refactor in small steps**
   - Extract functions/methods
   - Rename for clarity
   - Remove dead code
   - Simplify conditionals
   - Each step: run tests to confirm green

4. **Verify** — the external API/interface is unchanged; all tests still pass

5. **Report changes made** — list what was changed and why

## Rules
- Never add new features during a refactor
- If tests don't exist, write them first (use /tdd)
- Commit before and after each significant refactor step
