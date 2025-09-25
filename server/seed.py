#!/usr/bin/env python3
from app import create_app, db
from models import User, Goal, Workout, Exercise, ExerciseLog

app = create_app()

with app.app_context():
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    # ---------------- USERS ----------------
    user1 = User(username="samuel")
    user2 = User(username="jane")

    db.session.add_all([user1, user2])
    db.session.commit()

    # ---------------- GOALS ----------------
    goal1 = Goal(name="Strength Training")
    goal2 = Goal(name="Cardio Endurance")

    # Link goals to users
    user1.goals.extend([goal1, goal2])
    user2.goals.append(goal1)

    db.session.add_all([goal1, goal2])
    db.session.commit()

    # ---------------- WORKOUTS ----------------
    workout1 = Workout(
        title="Leg Day",
        date="2025-09-20",
        notes="Focused on squats and lunges",
        user_id=user1.id
    )
    workout2 = Workout(
        title="Morning Run",
        date="2025-09-21",
        notes="5km around the park",
        user_id=user1.id
    )
    workout3 = Workout(
        title="Upper Body Strength",
        date="2025-09-21",
        notes="Bench press and pull-ups",
        user_id=user2.id
    )

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    # ---------------- EXERCISES ----------------
    squat = Exercise(exercise_name="Squat", goal_id=goal1.id)
    bench = Exercise(exercise_name="Bench Press", goal_id=goal1.id)
    run = Exercise(exercise_name="Running", goal_id=goal2.id)

    db.session.add_all([squat, bench, run])
    db.session.commit()

    # ---------------- EXERCISE LOGS ----------------
    log1 = ExerciseLog(sets=4, reps=10, weight=80, workout_id=workout1.id, exercise_id=squat.id)
    log2 = ExerciseLog(sets=3, reps=8, weight=60, workout_id=workout3.id, exercise_id=bench.id)
    log3 = ExerciseLog(sets=1, reps=1, weight=None, workout_id=workout2.id, exercise_id=run.id)

    db.session.add_all([log1, log2, log3])
    db.session.commit()

    print("Database seeded successfully! ✅")
