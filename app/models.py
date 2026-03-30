from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    sessions = db.relationship('Session', backref='user', lazy=True,
                               cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.is_admin is None:
            self.is_admin = False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class WorkoutDay(db.Model):
    __tablename__ = 'workout_days'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    week_day = db.Column(db.String(10), nullable=False)

    exercises = db.relationship('Exercise', backref='day', lazy=True)
    sessions = db.relationship('Session', backref='day', lazy=True)

    def __repr__(self):
        return f'<Day {self.name} - {self.label}>'


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('workout_days.id'), nullable=False)
    working_sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.String(20), nullable=False)
    is_superset = db.Column(db.Boolean, default=False)
    superset_group = db.Column(db.String(5), nullable=True)
    order = db.Column(db.Integer, nullable=False)

    substitutions = db.relationship('Substitution', backref='exercise', lazy=True)
    set_logs = db.relationship('SetLog', backref='exercise', lazy=True)

    def __repr__(self):
        return f'<Exercise {self.name}>'


class Substitution(db.Model):
    __tablename__ = 'substitutions'

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    option_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sub {self.name} for exercise {self.exercise_id}>'


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    day_id = db.Column(db.Integer, db.ForeignKey('workout_days.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    set_logs = db.relationship('SetLog', backref='session', lazy=True,
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Session {self.id} on {self.date}>'


class SetLog(db.Model):
    __tablename__ = 'set_logs'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reps_completed = db.Column(db.Integer, nullable=False)
    sub_id = db.Column(db.Integer, db.ForeignKey('substitutions.id'), nullable=True)

    def __repr__(self):
        return f'<SetLog session={self.session_id} exercise={self.exercise_id} set={self.set_number}>'
