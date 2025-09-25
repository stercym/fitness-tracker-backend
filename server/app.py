#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from models import User, Goal, Workout, Exercise, ExerciseLog

    @app.route('/')
    def index():
        return jsonify({"message": "Fitness Tracker API is running!"})

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        new_user = User(name=data["name"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    @app.route("/goals", methods=["GET"])
    def get_goals():
        goals = Goal.query.all()
        return jsonify([{"id": g.id, "name": g.name} for g in goals])

    @app.route("/goals", methods=["POST"])
    def create_goal():
        data = request.get_json()
        new_goal = Goal(name=data["name"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"message": "Goal created successfully"}), 201

    @app.route("/exercises", methods=["GET"])
    def get_exercises():
        exercises = Exercise.query.all()
        return jsonify([
            {"id": e.id, "name": e.name, "goal_id": e.goal_id} for e in exercises
        ])

    @app.route("/exercises", methods=["POST"])
    def create_exercise():
        data = request.get_json()
        new_exercise = Exercise(name=data["name"], goal_id=data["goal_id"])
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify({"message": "Exercise created successfully"}), 201

    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.all()
        return jsonify([
            {"id": w.id, "date": w.date, "user_id": w.user_id} for w in workouts
        ])

    @app.route("/workouts", methods=["POST"])
    def create_workout():
        data = request.get_json()
        new_workout = Workout(date=data["date"], user_id=data["user_id"])
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"message": "Workout created successfully"}), 201

    @app.route("/exercise_logs", methods=["GET"])
    def get_logs():
        logs = ExerciseLog.query.all()
        return jsonify([
            {
                "id": log.id,
                "sets": log.sets,
                "reps": log.reps,
                "weight": log.weight,
                "workout_id": log.workout_id,
                "exercise_id": log.exercise_id
            } for log in logs
        ])

    @app.route("/exercise_logs", methods=["POST"])
    def create_log():
        data = request.get_json()
        new_log = ExerciseLog(
            sets=data["sets"],
            reps=data["reps"],
            weight=data.get("weight", 0),
            workout_id=data["workout_id"],
            exercise_id=data["exercise_id"]
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Exercise log created successfully."}), 201

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
