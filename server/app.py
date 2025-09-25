#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from extensions import db, migrate 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from models import User, Goal, Workout, Exercise, ExerciseLog

    @app.route("/")
    def index():
        return jsonify({"message": "Fitness Tracker API is running!"})

    #  PROGRESS ROUTE 
    @app.route("/api/progress/<int:user_id>", methods=["GET"])
    def get_progress(user_id):
        user = User.query.get_or_404(user_id)

        total_workouts = Workout.query.filter_by(user_id=user_id).count()

        logs_by_goal = []
        for goal in user.goals:
            total_exercises = (
                db.session.query(ExerciseLog)
                .join(Exercise, Exercise.id == ExerciseLog.exercise_id)
                .join(Workout, Workout.id == ExerciseLog.workout_id)
                .filter(Workout.user_id == user_id, Exercise.goal_id == goal.id)
                .count()
            )
            logs_by_goal.append({
                "goal_id": goal.id,
                "goal_name": goal.name,
                "total_exercises": total_exercises,
            })

        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "total_workouts": total_workouts,
            "logs_by_goal": logs_by_goal,
        })

    # USERS 
    @app.route("/api/users", methods=["GET"])
    def get_users():
        return jsonify([u.to_dict() for u in User.query.all()])

    @app.route("/api/users/<int:id>", methods=["GET"])
    def get_user(id):
        return jsonify(User.query.get_or_404(id).to_dict())

    @app.route("/api/users", methods=["POST"])
    def create_user():
        data = request.json
        user = User(username=data["username"])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @app.route("/api/users/<int:id>", methods=["PUT"])
    def update_user(id):
        user = User.query.get_or_404(id)
        data = request.json
        user.username = data.get("username", user.username)
        db.session.commit()
        return jsonify(user.to_dict())

    @app.route("/api/users/<int:id>", methods=["DELETE"])
    def delete_user(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})
    
    #  GOALS 
    @app.route("/api/goals", methods=["GET"])
    def get_goals():
        return jsonify([g.to_dict() for g in Goal.query.all()])

    @app.route("/api/goals/<int:id>", methods=["GET"])
    def get_goal(id):
        return jsonify(Goal.query.get_or_404(id).to_dict())

    @app.route("/api/goals", methods=["POST"])
    def create_goal():
        data = request.json
        goal = Goal(name=data["name"])
        db.session.add(goal)
        db.session.commit()
        return jsonify(goal.to_dict()), 201

    @app.route("/api/goals/<int:id>", methods=["PUT"])
    def update_goal(id):
        goal = Goal.query.get_or_404(id)
        data = request.json
        goal.name = data.get("name", goal.name)
        db.session.commit()
        return jsonify(goal.to_dict())

    @app.route("/api/goals/<int:id>", methods=["DELETE"])
    def delete_goal(id):
        goal = Goal.query.get_or_404(id)
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"message": "Goal deleted"})

    #  WORKOUTS 
    @app.route("/api/workouts", methods=["GET"])
    def get_workouts():
        return jsonify([w.to_dict() for w in Workout.query.all()])

    @app.route("/api/workouts/<int:id>", methods=["GET"])
    def get_workout(id):
        return jsonify(Workout.query.get_or_404(id).to_dict())

    @app.route("/api/workouts", methods=["POST"])
    def create_workout():
        data = request.json
        workout = Workout(
            title=data["title"],
            date=data["date"],
            notes=data.get("notes", ""),
            user_id=data["user_id"]
        )
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout.to_dict()), 201

    @app.route("/api/workouts/<int:id>", methods=["PUT"])
    def update_workout(id):
        workout = Workout.query.get_or_404(id)
        data = request.json
        workout.title = data.get("title", workout.title)
        workout.date = data.get("date", workout.date)
        workout.notes = data.get("notes", workout.notes)
        db.session.commit()
        return jsonify(workout.to_dict())

    @app.route("/api/workouts/<int:id>", methods=["DELETE"])
    def delete_workout(id):
        workout = Workout.query.get_or_404(id)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": "Workout deleted"})


    # EXERCISES 
    @app.route("/api/exercises", methods=["GET"])
    def get_exercises():
        return jsonify([e.to_dict() for e in Exercise.query.all()])

    @app.route("/api/exercises/<int:id>", methods=["GET"])
    def get_exercise(id):
        return jsonify(Exercise.query.get_or_404(id).to_dict())

    @app.route("/api/exercises", methods=["POST"])
    def create_exercise():
        data = request.json
        exercise = Exercise(
            exercise_name=data["exercise_name"],
            goal_id=data.get("goal_id")
        )
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise.to_dict()), 201

    @app.route("/api/exercises/<int:id>", methods=["PUT"])
    def update_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        data = request.json
        exercise.exercise_name = data.get("exercise_name", exercise.exercise_name)
        exercise.goal_id = data.get("goal_id", exercise.goal_id)
        db.session.commit()
        return jsonify(exercise.to_dict())

    @app.route("/api/exercises/<int:id>", methods=["DELETE"])
    def delete_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted"})
    

    #  EXERCISE LOGS
    @app.route("/api/exercise_logs", methods=["GET"])
    def get_exercise_logs():
        return jsonify([log.to_dict() for log in ExerciseLog.query.all()])

    @app.route("/api/exercise_logs/<int:id>", methods=["GET"])
    def get_exercise_log(id):
        return jsonify(ExerciseLog.query.get_or_404(id).to_dict())

    @app.route("/api/exercise_logs", methods=["POST"])
    def create_exercise_log():
        data = request.json
        log = ExerciseLog(
            sets=data["sets"],
            reps=data["reps"],
            weight=data.get("weight"),
            workout_id=data["workout_id"],
            exercise_id=data["exercise_id"]
        )
        db.session.add(log)
        db.session.commit()
        return jsonify(log.to_dict()), 201

    @app.route("/api/exercise_logs/<int:id>", methods=["PUT"])
    def update_exercise_log(id):
        log = ExerciseLog.query.get_or_404(id)
        data = request.json
        log.sets = data.get("sets", log.sets)
        log.reps = data.get("reps", log.reps)
        log.weight = data.get("weight", log.weight)
        log.workout_id = data.get("workout_id", log.workout_id)
        log.exercise_id = data.get("exercise_id", log.exercise_id)
        db.session.commit()
        return jsonify(log.to_dict())

    @app.route("/api/exercise_logs/<int:id>", methods=["DELETE"])
    def delete_exercise_log(id):
        log = ExerciseLog.query.get_or_404(id)
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "ExerciseLog deleted"})
    

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


