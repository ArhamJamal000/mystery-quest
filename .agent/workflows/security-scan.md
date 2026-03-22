---
description: Run a security audit covering OWASP Top 10, secrets exposure, auth, and input validation
---

# /security-scan — Security Audit Workflow

Perform a security review of the codebase or specified files.

## Usage
`/security-scan` — scan the entire project  
`/security-scan <file or folder>` — scan specific target

## Checklist

### 🔑 Secrets & Credentials
- [ ] No API keys, passwords, or tokens hardcoded in source files
- [ ] `.env` files are in `.gitignore`
- [ ] No secrets in git history (check recent commits if relevant)

### 🔐 Authentication & Authorization
- [ ] All protected routes/endpoints require authentication
- [ ] Authorization checks verify the user owns the resource (not just that they're logged in)
- [ ] Passwords are hashed with bcrypt/argon2 (never MD5/SHA1)
- [ ] JWT tokens validated for expiry and signature

### 💉 Injection Attacks
- [ ] SQL queries use parameterized queries or ORM (no string concatenation)
- [ ] User input is never eval()'d or exec()'d
- [ ] File paths constructed from user input are sanitized

### 🌐 Web/API Security
- [ ] CORS is restrictive (not `*` in production)
- [ ] CSRF tokens used on state-changing forms
- [ ] Rate limiting on auth endpoints
- [ ] File uploads validate MIME type and size

### 📦 Dependencies
- [ ] Run `npm audit` / `pip-audit` / equivalent
- [ ] No known critical CVEs in direct dependencies

## Output Format
```
## Security Scan Report

### 🔴 Critical (fix immediately)
### 🟡 High (fix before release)  
### 🟢 Low (monitor)
### ✅ Passed checks
```
