from app import db
from datetime import datetime

class WorkoutDay(db.Model):
    __tablename__ = 'workout_days'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1), nullable=False)        # A, B, C, D
    label = db.Column(db.String(50), nullable=False)      # e.g. "Lower 1"
    week_day = db.Column(db.String(10), nullable=False)   # e.g. "Monday"

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
    reps = db.Column(db.String(20), nullable=False)       # e.g. "4-6", "10-12"
    is_superset = db.Column(db.Boolean, default=False)    # True for A1/A2 pairs
    superset_group = db.Column(db.String(5), nullable=True)  # e.g. "A", "B"
    order = db.Column(db.Integer, nullable=False)         # display order within day

    substitutions = db.relationship('Substitution', backref='exercise', lazy=True)
    set_logs = db.relationship('SetLog', backref='exercise', lazy=True)

    def __repr__(self):
        return f'<Exercise {self.name}>'


class Substitution(db.Model):
    __tablename__ = 'substitutions'

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    option_number = db.Column(db.Integer, nullable=False)  # 1 or 2

    def __repr__(self):
        return f'<Sub {self.name} for exercise {self.exercise_id}>'


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('workout_days.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    set_logs = db.relationship('SetLog', backref='session', lazy=True)

    def __repr__(self):
        return f'<Session {self.id} on {self.date}>'


class SetLog(db.Model):
    __tablename__ = 'set_logs'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)     # 1, 2, 3, 4...
    weight = db.Column(db.Float, nullable=False)           # in kg
    reps_completed = db.Column(db.Integer, nullable=False)
    sub_id = db.Column(db.Integer, db.ForeignKey('substitutions.id'), nullable=True)  # null = did main exercise

    def __repr__(self):
        return f'<SetLog session={self.session_id} exercise={self.exercise_id} set={self.set_number}>'