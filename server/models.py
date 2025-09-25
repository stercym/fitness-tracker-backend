from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many User <-> Goal
user_goals = db.Table(
    "user_goals",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)

    # Relationships
    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan")
    goals = db.relationship("Goal", secondary=user_goals, back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "goals": [goal.id for goal in self.goals],
            "workouts": [workout.id for workout in self.workouts],
        }


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    users = db.relationship("User", secondary=user_goals, back_populates="goals")
    exercises = db.relationship("Exercise", backref="goal", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [user.id for user in self.users],
            "exercises": [exercise.id for exercise in self.exercises],
        }


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, default="")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    exercises = db.relationship("ExerciseLog", backref="workout", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "notes": self.notes,
            "user_id": self.user_id,
            "exercises": [log.id for log in self.exercises],
        }


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(50), nullable=False)

    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "exercise_name": self.exercise_name,
            "goal_id": self.goal_id,
        }


class ExerciseLog(db.Model):
    __tablename__ = "exercise_logs"

    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
        }

