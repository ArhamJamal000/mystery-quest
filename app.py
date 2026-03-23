import os
from flask import Flask, session, redirect, url_for, render_template, request, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Team, LevelAttempt, GameSettings
import json
from datetime import datetime

def get_question_banks():
    json_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    if not os.path.exists(json_path):
        from questions import QUESTION_BANKS
        return QUESTION_BANKS
    with open(json_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    banks = {}
    for pool, levels in raw.items():
        banks[pool] = {}
        for level_str, data in levels.items():
            banks[pool][int(level_str)] = data
    return banks
import random

# PRE-EVENT CHECKLIST:
# [ ] Change ADMIN_PASSWORD in Render environment variables
# [ ] Set up UptimeRobot to ping app URL every 5 minutes
# [ ] Visit site 10 minutes before event to warm up cold start
# [ ] Run /admin/questions — verify all 15 questions are correct
# [ ] Test full flow with a dummy team
# [ ] Keep admin dashboard open on organizer's laptop during event
# [ ] Have CSV export ready as backup

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if not GameSettings.query.first():
        db.session.add(GameSettings())
        db.session.commit()

POOLS = ['A', 'B', 'C']

def assign_pool():
    counts = {p: Team.query.filter_by(question_pool=p).count() for p in POOLS}
    return min(counts, key=counts.get)

def check_time_limit(team):
    settings = GameSettings.query.first()
    if not team.start_time:
        return False
    elapsed_mins = (datetime.utcnow() - team.start_time).total_seconds() / 60
    if elapsed_mins > settings.time_limit_mins:
        team.disqualified = True
        if not team.end_time:
            team.end_time = datetime.utcnow()
        db.session.commit()
        return True
    return False

WRONG_MESSAGES = [
    "Nahi bhai nahi! Mogambo khush nahi hua 😤",
    "Itna bhi nahi pata? +30 seconds le lo 😭",
    "Bhai seedha jawab do! Penalty lag gayi 🙄",
    "Wrong! Yeh Kaun Banega Crorepati nahi hai 😂",
    "Arre yaar... Computer ji, lock kar do! ⏱️"
]

def validate_answer(team, level, submitted):
    bank = get_question_banks()[team.question_pool][level]
    correct = bank['answer'].strip().lower()
    if submitted.strip().lower() == correct:
        return True
    return False

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.get('csrf_token', None)
        req_token = request.form.get('csrf_token') or request.headers.get('X-CSRFToken')
        if not token or token != req_token:
            # Return JSON for AJAX requests so client-side handler can parse it
            if request.headers.get('X-CSRFToken') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "message": "Session expired. Please refresh the page."}), 403
            return "CSRF token missing or incorrect", 403

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = os.urandom(24).hex()
    return session['csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

# ----- PLAYER ROUTES -----

@app.route('/')
def index():
    if 'team_id' in session:
        team = db.session.get(Team, session['team_id'])
        if team:
            if team.disqualified:
                return redirect(url_for('timeout'))
            if team.completed:
                return redirect(url_for('victory'))
            settings = GameSettings.query.first()
            if not settings.game_active:
                return redirect(url_for('lobby'))
            return redirect(url_for('level', n=team.current_level))
    settings = GameSettings.query.first()
    return render_template('landing.html', game_active=settings.game_active)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    roll_number = request.form.get('roll_number')

    if not name or not roll_number:
        return "Please fill all fields", 400

    # Check if existing team
    team = Team.query.filter_by(roll_number=roll_number).first()
    if team:
        session['team_id'] = team.id
        return redirect(url_for('index'))

    # Create new team
    pool = assign_pool()
    new_team = Team(
        name=name,
        roll_number=roll_number,
        question_pool=pool,
        start_time=None
    )
    db.session.add(new_team)
    try:
        db.session.commit()
        session['team_id'] = new_team.id
        return redirect(url_for('confirm'))
    except Exception as e:
        db.session.rollback()
        return "Error registering. Roll number might exist.", 400

@app.route('/confirm')
def confirm():
    if 'team_id' not in session:
        return redirect(url_for('index'))
    team = db.session.get(Team, session['team_id'])
    if not team:
        return redirect(url_for('index'))
    return render_template('confirm.html', team=team)

@app.route('/level/<int:n>')
def level(n):
    if 'team_id' not in session:
        return redirect(url_for('index'))
    team = db.session.get(Team, session['team_id'])
    if not team:
        session.pop('team_id', None)
        return redirect(url_for('index'))
    
    settings = GameSettings.query.first()
    if not settings.game_active:
        return redirect(url_for('lobby'))
        
    if team.disqualified:
        return redirect(url_for('timeout'))
    if team.completed:
        return redirect(url_for('victory'))
        
    if not team.start_time:
        team.start_time = datetime.utcnow()
        db.session.commit()
    
    if check_time_limit(team):
        return redirect(url_for('timeout'))

    if team.current_level != n:
        return "Forbidden", 403

    question_data = get_question_banks()[team.question_pool][n]
    safe_data = {k: v for k, v in question_data.items() if k != 'answer'}

    return render_template('level.html', team=team, level=n, data=safe_data)

@app.route('/level/<int:n>/submit', methods=['POST'])
def submit_answer(n):
    if 'team_id' not in session:
        return jsonify({"success": False, "redirect": url_for('index')})
    team = db.session.get(Team, session['team_id'])
    
    if team.current_level != n or team.disqualified or team.completed:
        return jsonify({"success": False, "redirect": url_for('index')})

    if check_time_limit(team):
        return jsonify({"success": False, "redirect": url_for('timeout')})

    answer = request.form.get('answer', '')
    
    attempt = LevelAttempt.query.filter_by(team_id=team.id, level=n).first()
    if not attempt:
        attempt = LevelAttempt(team_id=team.id, level=n, attempts=0, wrong_count=0)
        db.session.add(attempt)
        db.session.flush()  # assign defaults before incrementing

    attempt.attempts += 1

    settings = GameSettings.query.first()

    if validate_answer(team, n, answer):
        attempt.solved_at = datetime.utcnow()
        team.current_level += 1
        
        if team.current_level > 5:
            team.completed = True
            team.end_time = datetime.utcnow()
            total_seconds = int((team.end_time - team.start_time).total_seconds())
            team.total_time = total_seconds + team.penalty_secs
            db.session.commit()
            return jsonify({"success": True, "redirect": url_for('victory')})
        else:
            db.session.commit()
            return jsonify({"success": True, "redirect": url_for('level', n=team.current_level)})
    else:
        attempt.wrong_count += 1
        team.penalty_secs += settings.penalty_secs
        db.session.commit()
        msg = random.choice(WRONG_MESSAGES)
        return jsonify({
            "success": False, 
            "message": f"{msg} (+{settings.penalty_secs}s penalty)"
        })

@app.route('/victory')
def victory():
    if 'team_id' not in session:
        return redirect(url_for('index'))
    team = db.session.get(Team, session['team_id'])
    if not team or not team.completed:
        return redirect(url_for('index'))
    
    rank = Team.query.filter_by(completed=True).filter(Team.total_time < team.total_time).count() + 1
    raw_time = int((team.end_time - team.start_time).total_seconds()) if team.end_time else 0
    return render_template('victory.html', team=team, rank=rank, raw_time=raw_time)

@app.route('/timeout')
def timeout():
    if 'team_id' not in session:
        return redirect(url_for('index'))
    team = db.session.get(Team, session['team_id'])
    if not team:
        session.pop('team_id', None)
        return redirect(url_for('index'))
    return render_template('timeout.html', team=team)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/lobby')
def lobby():
    if 'team_id' not in session:
        return redirect(url_for('index'))
    team = db.session.get(Team, session['team_id'])
    if not team:
        session.pop('team_id', None)
        return redirect(url_for('index'))
        
    settings = GameSettings.query.first()
    if settings.game_active:
        return redirect(url_for('index'))
        
    teams = Team.query.order_by(Team.registered_at.desc()).all()
    return render_template('lobby.html', team=team, teams=teams)

@app.route('/api/lobby-status')
def lobby_status():
    settings = GameSettings.query.first()
    teams = Team.query.order_by(Team.registered_at.desc()).all()
    team_list = [{"name": t.name} for t in teams]
    return jsonify({
        "game_active": settings.game_active,
        "teams": team_list
    })

# ----- API ROUTES -----

@app.route('/api/leaderboard')
def api_leaderboard():
    completed = Team.query.filter_by(completed=True, disqualified=False).order_by(Team.total_time.asc()).all()
    incomplete = Team.query.filter_by(completed=False, disqualified=False).all()
    
    now = datetime.utcnow()
    def get_elapsed(t):
        if not t.start_time: return 0
        return (now - t.start_time).total_seconds()

    incomplete.sort(key=lambda t: (-t.current_level, get_elapsed(t)))

    disqualified = Team.query.filter_by(disqualified=True).all()
    
    results = []
    rank = 1
    for t in completed:
        results.append({
            "rank": rank,
            "name": t.name,
            "levels_completed": t.current_level - 1,
            "adjusted_time": t.total_time,
            "status": "Completed"
        })
        rank += 1
        
    for t in incomplete:
        raw = get_elapsed(t)
        adj = int(raw) + t.penalty_secs
        results.append({
            "rank": "-",
            "name": t.name,
            "levels_completed": t.current_level - 1,
            "adjusted_time": adj,
            "status": "Playing"
        })
        
    for t in disqualified:
        results.append({
             "rank": "-",
             "name": t.name,
             "levels_completed": t.current_level - 1,
             "adjusted_time": "-",
             "status": "Disqualified"
        })
    return jsonify(results)

@app.route('/api/status')
def api_status():
    if 'team_id' not in session:
        return jsonify({"error": "No session"}), 403
    team = db.session.get(Team, session['team_id'])
    if not team:
        return jsonify({"error": "Invalid team"}), 403
    
    now = datetime.utcnow()
    elapsed = int((now - team.start_time).total_seconds()) if team.start_time else 0
    settings = GameSettings.query.first()
    return jsonify({
        "level": team.current_level,
        "elapsed_secs": elapsed,
        "penalty_secs": team.penalty_secs,
        "total_adjusted": elapsed + team.penalty_secs,
        "time_limit_secs": settings.time_limit_mins * 60
    })

admin_failures = {}

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    ip = request.remote_addr
    now = datetime.utcnow()
    
    if ip in admin_failures:
        admin_failures[ip] = [t for t in admin_failures[ip] if (now - t).total_seconds() < 600]
        if len(admin_failures[ip]) >= 5:
            return "Too many failed attempts. Try again in 10 minutes.", 429

    if request.method == 'POST':
        password_attempt = request.form.get('password', '')
        true_password = os.environ.get('ADMIN_PASSWORD', 'changeme_before_event')
        
        is_valid = False
        if true_password.startswith('pbkdf2:sha256:'):
            is_valid = check_password_hash(true_password, password_attempt)
        else:
            is_valid = (password_attempt == true_password)
            
        if is_valid:
            session['admin'] = True
            if ip in admin_failures:
                del admin_failures[ip]
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin password")
            if ip not in admin_failures:
                admin_failures[ip] = []
            admin_failures[ip].append(now)
            
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    settings = GameSettings.query.first()
    teams = Team.query.all()
    pool_counts = {p: Team.query.filter_by(question_pool=p).count() for p in POOLS}
    
    now = datetime.utcnow()
    event_timer = int((now - settings.event_started_at).total_seconds()) if settings.event_started_at else 0
    
    # Manual sort for dashboard similar to leaderboard
    def get_elapsed(t):
        if not t.start_time: return 0
        return (now - t.start_time).total_seconds()
    
    return render_template('admin/dashboard.html', settings=settings, teams=teams, pool_counts=pool_counts, event_timer=event_timer, get_elapsed=get_elapsed)

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    settings = GameSettings.query.first()
    
    if request.method == 'POST':
        try:
            time_limit = int(request.form.get('time_limit_mins', settings.time_limit_mins))
            penalty = int(request.form.get('penalty_secs', settings.penalty_secs))
            settings.time_limit_mins = time_limit
            settings.penalty_secs = penalty
            db.session.commit()
            flash("Settings updated successfully.")
        except ValueError:
            flash("Invalid input. Please enter numbers.")
        return redirect(url_for('admin_settings'))
        
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/questions')
def admin_questions():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    settings = GameSettings.query.first()
    return render_template('admin/questions.html', settings=settings, banks=get_question_banks())

@app.route('/admin/questions/edit', methods=['GET', 'POST'])
def admin_questions_edit():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    json_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    
    if request.method == 'POST':
        new_json = request.form.get('questions_json')
        try:
            parsed = json.loads(new_json)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=4)
            flash("Questions updated successfully!")
            return redirect(url_for('admin_questions'))
        except Exception as e:
            flash(f"Error parsing JSON: {str(e)}")
            
    if not os.path.exists(json_path):
        from questions import QUESTION_BANKS
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(QUESTION_BANKS, f, indent=4)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        current_json = f.read()
    return render_template('admin/questions_edit.html', raw_json=current_json)

@app.route('/admin/start-event', methods=['POST'])
def start_event():
    if not session.get('admin'): return "Forbidden", 403
    settings = GameSettings.query.first()
    settings.game_active = True
    if not settings.event_started_at:
        settings.event_started_at = datetime.utcnow()
    db.session.commit()
    flash("Event Started!")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/force-advance/<int:id>', methods=['POST'])
def force_advance(id):
    if not session.get('admin'): return "Forbidden", 403
    team = db.session.get(Team, id)
    if team and not team.completed and not team.disqualified:
        team.current_level += 1
        if team.current_level > 5:
            team.completed = True
            team.end_time = datetime.utcnow()
            total_seconds = int((team.end_time - team.start_time).total_seconds())
            team.total_time = total_seconds + team.penalty_secs
        db.session.commit()
        flash(f"Advanced {team.name} to level {team.current_level}")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/kick/<int:id>', methods=['POST'])
def kick_team(id):
    if not session.get('admin'): return "Forbidden", 403
    team = db.session.get(Team, id)
    if team:
        team.disqualified = True
        db.session.commit()
        flash(f"Kicked {team.name}")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset', methods=['POST'])
def admin_reset():
    if not session.get('admin'): return "Forbidden", 403
    if request.form.get('confirm_text') == 'RESET':
        LevelAttempt.query.delete()
        Team.query.delete()
        settings = GameSettings.query.first()
        settings.game_active = False
        settings.event_started_at = None
        db.session.commit()
        flash("Game Reset successfully.")
    else:
        flash("Reset verification failed.")
    return redirect(url_for('admin_settings'))

@app.route('/admin/export')
def admin_export():
    if not session.get('admin'): return "Forbidden", 403
    import csv
    from io import StringIO
    from flask import Response
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Rank', 'Team Name', 'Roll No', 'Pool', 'Level Reached', 'Raw Time (s)', 'Penalty (s)', 'Adjusted Time (s)', 'Status'])
    
    completed = Team.query.filter_by(completed=True, disqualified=False).order_by(Team.total_time.asc()).all()
    incomplete = Team.query.filter_by(completed=False, disqualified=False).all()
    disqualified = Team.query.filter_by(disqualified=True).all()
    
    now = datetime.utcnow()
    def get_elapsed(t):
        if not t.start_time: return 0
        return (now - t.start_time).total_seconds()

    incomplete.sort(key=lambda t: (-t.current_level, get_elapsed(t)))
    
    rank = 1
    for t in completed:
        raw = int((t.end_time - t.start_time).total_seconds()) if t.start_time and t.end_time else 0
        writer.writerow([rank, t.name, t.roll_number, t.question_pool, t.current_level, raw, t.penalty_secs, t.total_time, 'Completed'])
        rank += 1
    for t in incomplete:
        raw_time = int(get_elapsed(t))
        adj = raw_time + t.penalty_secs
        writer.writerow(['-', t.name, t.roll_number, t.question_pool, t.current_level, raw_time, t.penalty_secs, adj, 'Playing'])
    for t in disqualified:
        raw_time = int(get_elapsed(t))
        writer.writerow(['-', t.name, t.roll_number, t.question_pool, t.current_level, raw_time, t.penalty_secs, '-', 'Disqualified'])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=mystery_quest_export.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
