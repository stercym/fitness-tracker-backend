#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import User, Goal, Workout, Exercise, ExerciseLog

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return jsonify({"message": "Fitness Tracker API is running!"})

    return app

app = create_app()
