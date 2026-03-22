---
description: List all available global workflows and skills (the everything-claude-code equivalent)
---

# /help — Available Global Workflows & Skills

## 🔀 Workflows (slash commands)

| Command | Description |
|---|---|
| `/plan` | Plan a feature with a structured blueprint before coding |
| `/tdd` | Test-Driven Development (RED → GREEN → REFACTOR) |
| `/code-review` | Two-pass code review: quality + security |
| `/security-scan` | OWASP-based security audit |
| `/refactor` | Safe code refactoring without changing behaviour |
| `/debug` | Structured bug reproduction and fix |
| `/help` | Show this list |

## 🧠 Skills (auto-loaded when relevant)

| Skill | When used |
|---|---|
| `react-native-patterns` | React Native / Expo projects |
| `python-flask-patterns` | Flask backend projects |
| `git-workflow` | Any project — commits, branches, PRs |

## 📌 How to Use

Type any slash command in your message:

```
/plan "Add prayer notification scheduling"
/tdd
/code-review src/services/
/debug "The API returns 500 when the image is larger than 5MB"
/security-scan backend/
```

Skills are automatically referenced by Antigravity — you don't need to invoke them manually.
