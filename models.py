from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Team(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    roll_number   = db.Column(db.String(50), unique=True, nullable=False)
    question_pool = db.Column(db.String(1), nullable=False)   # 'A', 'B', or 'C'
    current_level = db.Column(db.Integer, default=1)
    penalty_secs  = db.Column(db.Integer, default=0)
    completed     = db.Column(db.Boolean, default=False)
    disqualified  = db.Column(db.Boolean, default=False)
    start_time    = db.Column(db.DateTime)
    end_time      = db.Column(db.DateTime, nullable=True)
    total_time    = db.Column(db.Integer, nullable=True)       # raw + penalty seconds
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class LevelAttempt(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    team_id     = db.Column(db.Integer, db.ForeignKey('team.id'))
    level       = db.Column(db.Integer)
    attempts    = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0)
    solved_at   = db.Column(db.DateTime, nullable=True)

class GameSettings(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    game_active      = db.Column(db.Boolean, default=False)
    event_started_at = db.Column(db.DateTime, nullable=True)
    time_limit_mins  = db.Column(db.Integer, default=90)
    penalty_secs     = db.Column(db.Integer, default=30)
