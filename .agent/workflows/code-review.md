---
description: Perform a thorough code review covering quality, security, performance, and maintainability
---

# /code-review — Code Review Workflow

Perform a two-pass review of the specified files or recent changes.

## Usage
`/code-review` — review all recently changed files  
`/code-review <file or folder>` — review specific target

## Pass 1: Correctness & Quality
- [ ] Logic errors or edge cases not handled
- [ ] Null/undefined/empty handling
- [ ] Error handling present and meaningful
- [ ] No dead code or unused imports
- [ ] Functions are single-responsibility
- [ ] Variable and function names are clear

## Pass 2: Security & Performance
- [ ] No hardcoded secrets or API keys
- [ ] SQL injection / XSS / CSRF risks (if applicable)
- [ ] No N+1 queries or unnecessary re-renders
- [ ] No blocking operations on the main thread
- [ ] Auth/permission checks are present where needed

## Output Format
Produce a structured report:

```
## Code Review Report

### 🔴 Critical Issues (must fix before merge)
- [file:line] description

### 🟡 Warnings (should fix)
- [file:line] description

### 🟢 Suggestions (optional improvements)
- [file:line] description

### ✅ Summary
[overall assessment in 1-2 sentences]
```

> [!NOTE]
> Always explain WHY something is an issue, not just what. Include a suggested fix when possible.
