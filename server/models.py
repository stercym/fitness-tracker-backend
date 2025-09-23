from app import db

# Association table for many-to-many User <-> Goal
user_goals = db.Table(
    "user_goals",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan")
    goals = db.relationship("Goal", secondary=user_goals, back_populates="users")

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    users = db.relationship("User", secondary=user_goals, back_populates="goals")
    exercises = db.relationship("Exercise", backref="goal", cascade="all, delete-orphan")

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
