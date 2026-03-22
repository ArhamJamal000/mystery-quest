---
name: git-workflow
description: Best practices for git commits, branching, PRs, and keeping a clean history
---

# Git Workflow Patterns

## Commit Message Format (Conventional Commits)

```
<type>(<scope>): <short summary>

[optional body]
[optional footer]
```

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code change (no feature/fix)
- `docs` — documentation only
- `test` — adding/fixing tests
- `chore` — build system, dependencies

**Examples:**
```
feat(auth): add JWT refresh token support
fix(upload): handle missing file extension gracefully
refactor(api): extract Gemini calls into service layer
```

## Branching Strategy

```
main          → production-ready, protected
develop       → integration branch
feature/xxx   → new features (branch from develop)
fix/xxx       → bugfixes (branch from main for hotfixes)
```

## Before Committing Checklist

- [ ] Run linter / type checker (`tsc --noEmit`, `flake8`, etc.)
- [ ] Run tests
- [ ] Remove all `console.log` / `print` debug statements
- [ ] No secrets or `.env` values committed

## Useful Commands

```bash
# Stage only specific changes (not whole files)
git add -p

# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Stash work in progress
git stash push -m "WIP: feature name"

# Interactive rebase to clean up commits before PR
git rebase -i HEAD~3

# See what changed in last commit
git show --stat
```

## .gitignore Essentials

```gitignore
# Secrets
.env
.env.local
*.pem

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/

# Build outputs
dist/
build/
*.apk
*.ipa

# IDE
.vscode/
.idea/
```
