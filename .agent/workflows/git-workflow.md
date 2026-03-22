---
description: Best practices for git commits, branching, PRs, and keeping a clean history
---

# /git-workflow — Git Workflow Guide

Follow these patterns for consistent and clean version control.

## Commit Message Format (Conventional Commits)
Use `<type>(<scope>): <short summary>`
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code change
- `docs` — documentation
- `test` — tests
- `chore` — build/deps

**Example:** `feat(auth): add JWT refresh token support`

## Branching Strategy
- `main` — production, protected
- `develop` — integration
- `feature/xxx` — new features (from develop)
- `fix/xxx` — hotfixes (from main)

## Checklist
- [ ] Run linter/tests
- [ ] Remove debug statements (`print`, `console.log`)
- [ ] No secrets in code

## Useful Commands
- `git add -p` — interactive stage
- `git reset --soft HEAD~1` — undo last commit
- `git stash push -m "msg"` — stash work
- `git rebase -i HEAD~3` — clean up commits
