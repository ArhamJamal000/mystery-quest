---
name: python-flask-patterns
description: Production patterns for Flask backends including SQLAlchemy, error handling, security, and API design
---

# Python / Flask Patterns

## App Factory Pattern

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or 'config.DevelopmentConfig')
    db.init_app(app)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
```

## Error Handling

Always register global error handlers:

```python
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Internal server error"), 500
```

## SQLAlchemy — Safe Queries

```python
# ✅ Safe — parameterized
user = User.query.filter_by(email=email).first()

# ❌ NEVER do this
user = db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

## File Upload Validation

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify(error="No file"), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify(error="Invalid file type"), 400
    # Save with secure_filename
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
```

## Environment & Secrets

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

## Concurrent API Calls (asyncio)

```python
import asyncio
import google.generativeai as genai

async def call_gemini_async(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, model.generate_content, prompt)

# Run multiple calls concurrently
results = await asyncio.gather(
    call_gemini_async(prompt1),
    call_gemini_async(prompt2),
)
```

## Security Checklist

- [ ] Use `flask-wtf` for CSRF protection
- [ ] Hash passwords with `werkzeug.security.generate_password_hash`
- [ ] Rate-limit with `flask-limiter`
- [ ] Never log secrets or user passwords
- [ ] Set `SESSION_COOKIE_SECURE=True` in production
