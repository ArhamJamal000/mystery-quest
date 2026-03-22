---
description: Plan a new feature or task with structured analysis and implementation blueprint
---

# /plan — Feature Planning Workflow

Use this when starting any new feature, bugfix, or refactor. Produces a structured implementation blueprint before writing any code.

## Steps

1. **Understand the request**
   - Restate the goal in your own words
   - Identify what files/components are involved
   - Ask ONE clarifying question if scope is ambiguous

2. **Research the codebase**
   - Read relevant existing files to understand patterns in use
   - Check for similar features already implemented
   - Note the tech stack and conventions

3. **Identify risks and dependencies**
   - List files that will change
   - Note any breaking changes
   - Flag security or performance concerns

4. **Produce an implementation_plan.md** in the `.gemini/antigravity/brain/<conversation-id>/` folder with:
   - Goal description
   - Files to create/modify/delete (grouped by component)
   - Step-by-step approach
   - Verification plan (how to test it works)

5. **Present the plan** and wait for user approval before writing any code.

> [!IMPORTANT]
> Do NOT write any implementation code during this workflow. Planning only.
