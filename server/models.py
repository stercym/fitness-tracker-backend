from app import db
from sqlalchemy_serializer import SerializerMixin

# Association table
user_goals = db.Table(
    "user_goals",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan")
    goals = db.relationship("Goal", secondary=user_goals, back_populates="users")

    # Prevents recursion
    serialize_rules = ("-workouts.user", "-goals.users")


class Goal(db.Model, SerializerMixin):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    users = db.relationship("User", secondary=user_goals, back_populates="goals")
    exercises = db.relationship("Exercise", backref="goal", cascade="all, delete-orphan")

    serialize_rules = ("-users.goals", "-exercises.goal")


class Workout(db.Model, SerializerMixin):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    exercises = db.relationship("ExerciseLog", backref="workout", cascade="all, delete-orphan")

    serialize_rules = ("-user.workouts", "-exercises.workout")


class Exercise(db.Model, SerializerMixin):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))

    serialize_rules = ("-goal.exercises", "-exercise_logs.exercise")


class ExerciseLog(db.Model, SerializerMixin):
    __tablename__ = "exercise_logs"

    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))

    serialize_rules = ("-workout.exercises", "-exercise.logs")
