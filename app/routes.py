from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import WorkoutDay, Exercise, Session, SetLog, Substitution
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    days = WorkoutDay.query.order_by(WorkoutDay.id).all()
    return render_template('index.html', days=days)


@main.route('/log/<int:day_id>', methods=['GET'])
@login_required
def log(day_id):
    day = WorkoutDay.query.get_or_404(day_id)
    exercises = Exercise.query.filter_by(day_id=day_id).order_by(Exercise.order).all()

    last_session = Session.query.filter_by(
        day_id=day_id, user_id=current_user.id
    ).order_by(Session.date.desc()).first()

    last_weights = {}
    if last_session:
        for log in last_session.set_logs:
            key = log.exercise_id
            if key not in last_weights:
                last_weights[key] = []
            last_weights[key].append({
                'set': log.set_number,
                'weight': log.weight,
                'reps': log.reps_completed,
                'sub': log.substitution.name if log.sub_id else None
            })

    return render_template('log.html',
                           day=day,
                           exercises=exercises,
                           last_weights=last_weights,
                           today=datetime.today().strftime('%Y-%m-%d'))


@main.route('/log/<int:day_id>', methods=['POST'])
@login_required
def log_submit(day_id):
    day = WorkoutDay.query.get_or_404(day_id)
    exercises = Exercise.query.filter_by(day_id=day_id).order_by(Exercise.order).all()

    notes = request.form.get('notes', '')
    date_str = request.form.get('date', datetime.today().strftime('%Y-%m-%d'))
    session_date = datetime.strptime(date_str, '%Y-%m-%d')

    new_session = Session(
        day_id=day_id,
        user_id=current_user.id,
        date=session_date,
        notes=notes
    )
    db.session.add(new_session)
    db.session.flush()

    for exercise in exercises:
        for set_num in range(1, exercise.working_sets + 1):
            weight_key = f'weight_{exercise.id}_set{set_num}'
            reps_key = f'reps_{exercise.id}_set{set_num}'
            sub_key = f'sub_{exercise.id}_set{set_num}'

            weight = request.form.get(weight_key)
            reps = request.form.get(reps_key)
            sub_id = request.form.get(sub_key)

            if not weight or not reps:
                continue

            set_log = SetLog(
                session_id=new_session.id,
                exercise_id=exercise.id,
                set_number=set_num,
                weight=float(weight),
                reps_completed=int(reps),
                sub_id=int(sub_id) if sub_id and sub_id != '0' else None
            )
            db.session.add(set_log)

    db.session.commit()
    flash('Session logged successfully!', 'success')
    return redirect(url_for('main.history', day_id=day_id))


@main.route('/history')
@login_required
def history_home():
    days = WorkoutDay.query.order_by(WorkoutDay.id).all()
    return render_template('history.html', days=days, sessions=None, selected_day=None)


@main.route('/history/<int:day_id>')
@login_required
def history(day_id):
    days = WorkoutDay.query.order_by(WorkoutDay.id).all()
    selected_day = WorkoutDay.query.get_or_404(day_id)
    sessions = Session.query.filter_by(
        day_id=day_id, user_id=current_user.id
    ).order_by(Session.date.desc()).all()

    exercises = Exercise.query.filter_by(day_id=day_id).order_by(Exercise.order).all()
    chart_data = {}
    for exercise in exercises:
        chart_data[exercise.name] = {'dates': [], 'weights': []}
        for session in reversed(sessions):
            logs = [l for l in session.set_logs if l.exercise_id == exercise.id]
            if logs:
                max_weight = max(l.weight for l in logs)
                chart_data[exercise.name]['dates'].append(
                    session.date.strftime('%d %b')
                )
                chart_data[exercise.name]['weights'].append(max_weight)

    return render_template('history.html',
                           days=days,
                           sessions=sessions,
                           selected_day=selected_day,
                           chart_data=chart_data,
                           exercises=exercises)
