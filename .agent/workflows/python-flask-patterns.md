---
description: Production patterns for Flask backends including SQLAlchemy, error handling, security, and API design
---

# /python-flask-patterns — Flask Best Practices

Use these patterns when building Flask applications.

## App Factory Pattern
Register blueprints and extensions in a `create_app` function.

## Error Handling
Use `@app.errorhandler` for common HTTP codes (400, 404, 500) to return JSON errors.

## SQLAlchemy — Safe Queries
- ✅ `User.query.filter_by(email=email).first()`
- ❌ `db.execute(f"... WHERE email = '{email}'")`

## File Upload Validation
Validate extensions and use `secure_filename`. Limit `MAX_CONTENT_LENGTH`.

## Security Checklist
- [ ] CSRF protection (`flask-wtf`)
- [ ] Password hashing (`werkzeug.security`)
- [ ] Rate limiting
- [ ] Production cookie settings (`SESSION_COOKIE_SECURE=True`)

## Async API Calls
Use `asyncio` and `run_in_executor` for concurrent Gemini/external API calls.
