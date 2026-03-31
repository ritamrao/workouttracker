from app import db
from app.models import WorkoutDay, Exercise, Substitution, User
from flask import current_app


def seed_data():
    # Seed admin user if no users exist
    if not User.query.first():
        admin = User(username='admin', is_admin=True)
        admin.set_password(current_app.config['ADMIN_PASSWORD'])
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")

    # Don't seed workout data if it already exists
    if WorkoutDay.query.first():
        return

    # ── DAY A – Lower 1 (Monday) ──────────────────────────────────────────
    day_a = WorkoutDay(name='A', label='Lower 1', week_day='Monday')
    db.session.add(day_a)
    db.session.flush()

    exercises_a = [
        Exercise(name='Hack Squat (Heavy)', day_id=day_a.id, working_sets=1,
                 reps='4-6', is_superset=False, superset_group=None, order=1),
        Exercise(name='Hack Squat (Back Off)', day_id=day_a.id, working_sets=1,
                 reps='8-10', is_superset=False, superset_group=None, order=2),
        Exercise(name='Seated Hamstring Curl', day_id=day_a.id, working_sets=1,
                 reps='10-12', is_superset=False, superset_group=None, order=3),
        Exercise(name='Standing Calf Raise', day_id=day_a.id, working_sets=2,
                 reps='10-12', is_superset=True, superset_group='A', order=4),
        Exercise(name='Hanging Leg Raise', day_id=day_a.id, working_sets=2,
                 reps='10-12', is_superset=True, superset_group='A', order=5),
    ]
    db.session.add_all(exercises_a)
    db.session.flush()

    subs_a = [
        Substitution(exercise_id=exercises_a[0].id, name='Machine Squat', option_number=1),
        Substitution(exercise_id=exercises_a[0].id, name='Leg Press', option_number=2),
        Substitution(exercise_id=exercises_a[1].id, name='Machine Squat', option_number=1),
        Substitution(exercise_id=exercises_a[1].id, name='Leg Press', option_number=2),
        Substitution(exercise_id=exercises_a[2].id, name='Nordic Ham Curl', option_number=1),
        Substitution(exercise_id=exercises_a[2].id, name='Lying Leg Curl', option_number=2),
        Substitution(exercise_id=exercises_a[3].id, name='Seated Calf Raise', option_number=1),
        Substitution(exercise_id=exercises_a[3].id, name='Leg Press Toe Press', option_number=2),
        Substitution(exercise_id=exercises_a[4].id, name='Roman Chair Crunch', option_number=1),
        Substitution(exercise_id=exercises_a[4].id, name='Reverse Crunch', option_number=2),
    ]
    db.session.add_all(subs_a)

    # ── DAY B – Lower 2 (Wednesday) ───────────────────────────────────────
    day_b = WorkoutDay(name='B', label='Lower 2', week_day='Wednesday')
    db.session.add(day_b)
    db.session.flush()

    exercises_b = [
        Exercise(name='Romanian Deadlift', day_id=day_b.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=1),
        Exercise(name='Leg Press', day_id=day_b.id, working_sets=3,
                 reps='10-12', is_superset=False, superset_group=None, order=2),
        Exercise(name='Leg Extension', day_id=day_b.id, working_sets=1,
                 reps='10-12', is_superset=False, superset_group=None, order=3),
        Exercise(name='Seated Calf Raise', day_id=day_b.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=4),
        Exercise(name='Cable Crunch', day_id=day_b.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=5),
    ]
    db.session.add_all(exercises_b)
    db.session.flush()

    subs_b = [
        Substitution(exercise_id=exercises_b[0].id, name='DB Romanian Deadlift', option_number=1),
        Substitution(exercise_id=exercises_b[0].id, name='45° Hyperextension', option_number=2),
        Substitution(exercise_id=exercises_b[1].id, name='Goblet Squat', option_number=1),
        Substitution(exercise_id=exercises_b[1].id, name='DB Walking Lunge', option_number=2),
        Substitution(exercise_id=exercises_b[2].id, name='DB Step-Up', option_number=1),
        Substitution(exercise_id=exercises_b[2].id, name='Goblet Squat', option_number=2),
        Substitution(exercise_id=exercises_b[3].id, name='Standing Calf Raise', option_number=1),
        Substitution(exercise_id=exercises_b[3].id, name='Leg Press Toe Press', option_number=2),
        Substitution(exercise_id=exercises_b[4].id, name='Machine Crunch', option_number=1),
        Substitution(exercise_id=exercises_b[4].id, name='Plate-Weighted Crunch', option_number=2),
    ]
    db.session.add_all(subs_b)

    # ── DAY C – Upper 1 (Thursday) ────────────────────────────────────────
    day_c = WorkoutDay(name='C', label='Upper 1', week_day='Thursday')
    db.session.add(day_c)
    db.session.flush()

    exercises_c = [
        Exercise(name='Flat DB Press (Heavy)', day_id=day_c.id, working_sets=1,
                 reps='4-6', is_superset=False, superset_group=None, order=1),
        Exercise(name='Flat DB Press (Back Off)', day_id=day_c.id, working_sets=1,
                 reps='8-10', is_superset=False, superset_group=None, order=2),
        Exercise(name='2-Grip Lat Pulldown', day_id=day_c.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=3),
        Exercise(name='Seated DB Shoulder Press', day_id=day_c.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=4),
        Exercise(name='Seated Cable Row', day_id=day_c.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=5),
        Exercise(name='EZ Bar Skull Crusher', day_id=day_c.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=6),
        Exercise(name='EZ Bar Curl', day_id=day_c.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=7),
    ]
    db.session.add_all(exercises_c)
    db.session.flush()

    subs_c = [
        Substitution(exercise_id=exercises_c[0].id, name='Machine Chest Press', option_number=1),
        Substitution(exercise_id=exercises_c[0].id, name='Weighted Dip', option_number=2),
        Substitution(exercise_id=exercises_c[1].id, name='Machine Chest Press', option_number=1),
        Substitution(exercise_id=exercises_c[1].id, name='Weighted Dip', option_number=2),
        Substitution(exercise_id=exercises_c[2].id, name='2-Grip Pull-up', option_number=1),
        Substitution(exercise_id=exercises_c[2].id, name='Machine Pulldown', option_number=2),
        Substitution(exercise_id=exercises_c[3].id, name='Machine Shoulder Press', option_number=1),
        Substitution(exercise_id=exercises_c[3].id, name='Standing DB Arnold Press', option_number=2),
        Substitution(exercise_id=exercises_c[4].id, name='Incline Chest-Supported DB Row', option_number=1),
        Substitution(exercise_id=exercises_c[4].id, name='Chest-Supported T-Bar Row', option_number=2),
        Substitution(exercise_id=exercises_c[5].id, name='Overhead Cable Triceps Extension', option_number=1),
        Substitution(exercise_id=exercises_c[5].id, name='DB French Press', option_number=2),
        Substitution(exercise_id=exercises_c[6].id, name='DB Curl', option_number=1),
        Substitution(exercise_id=exercises_c[6].id, name='Cable EZ Curl', option_number=2),
    ]
    db.session.add_all(subs_c)

    # ── DAY D – Upper 2 (Saturday) ────────────────────────────────────────
    day_d = WorkoutDay(name='D', label='Upper 2', week_day='Saturday')
    db.session.add(day_d)
    db.session.flush()

    exercises_d = [
        Exercise(name='Pendlay Row', day_id=day_d.id, working_sets=2,
                 reps='8-10', is_superset=False, superset_group=None, order=1),
        Exercise(name='Machine Shoulder Press', day_id=day_d.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=2),
        Exercise(name='Weighted Pullup', day_id=day_d.id, working_sets=2,
                 reps='8-10', is_superset=False, superset_group=None, order=3),
        Exercise(name='Cable Chest Press', day_id=day_d.id, working_sets=2,
                 reps='10-12', is_superset=False, superset_group=None, order=4),
        Exercise(name='Bayesian Cable Curl', day_id=day_d.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=5),
        Exercise(name='Triceps Pressdown', day_id=day_d.id, working_sets=2,
                 reps='12-15', is_superset=True, superset_group='A', order=6),
        Exercise(name='DB Lateral Raise', day_id=day_d.id, working_sets=1,
                 reps='12-15', is_superset=False, superset_group=None, order=7),
    ]
    db.session.add_all(exercises_d)
    db.session.flush()

    subs_d = [
        Substitution(exercise_id=exercises_d[0].id, name='T-Bar Row', option_number=1),
        Substitution(exercise_id=exercises_d[0].id, name='Seated Cable Row', option_number=2),
        Substitution(exercise_id=exercises_d[1].id, name='Seated DB Shoulder Press', option_number=1),
        Substitution(exercise_id=exercises_d[1].id, name='Standing DB Arnold Press', option_number=2),
        Substitution(exercise_id=exercises_d[2].id, name='Lat Pulldown', option_number=1),
        Substitution(exercise_id=exercises_d[2].id, name='Neutral-Grip Pullup', option_number=2),
        Substitution(exercise_id=exercises_d[3].id, name='Weighted Dip', option_number=1),
        Substitution(exercise_id=exercises_d[3].id, name='Flat DB Press', option_number=2),
        Substitution(exercise_id=exercises_d[4].id, name='DB Incline Curl', option_number=1),
        Substitution(exercise_id=exercises_d[4].id, name='DB Curl', option_number=2),
        Substitution(exercise_id=exercises_d[5].id, name='Cable Triceps Kickback', option_number=1),
        Substitution(exercise_id=exercises_d[5].id, name='DB Triceps Kickback', option_number=2),
        Substitution(exercise_id=exercises_d[6].id, name='Cable Lateral Raise', option_number=1),
        Substitution(exercise_id=exercises_d[6].id, name='Machine Lateral Raise', option_number=2),
    ]
    db.session.add_all(subs_d)

    db.session.commit()
    print("Database seeded successfully!")