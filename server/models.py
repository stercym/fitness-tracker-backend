from app import db

# Association table for many-to-many User <-> Goal
class UserGoal(db.Model):
    __tablename__ = "user_goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    target_date = db.Column(db.String(20), nullable=True)
    # shows progress in percentage
    progress = db.Column(db.Float, default=0.0) 

    # Relationships
    user = db.relationship("User", back_populates="user_goals")
    goal = db.relationship("Goal", back_populates="user_goals")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan")
    user_goals = db.relationship("UserGoal", back_populates="user", cascade="all, delete-orphan")

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    exercises = db.relationship("Exercise", backref="goal", cascade="all, delete-orphan")
    user_goals = db.relationship("UserGoal", back_populates="goal", cascade="all, delete-orphan")

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    exercises = db.relationship("ExerciseLog", backref="workout", cascade="all, delete-orphan")

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))

class ExerciseLog(db.Model):
    __tablename__ = "exercise_logs"

    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))
