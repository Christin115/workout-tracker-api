#!/usr/bin/env python3

from pathlib import Path

from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import Exercise, Workout, WorkoutExercise, db
from server.schemas import (
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "instance" / "app.db"
DATABASE_PATH.parent.mkdir(exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{DATABASE_PATH}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


def json_error(message, status_code):
    return make_response(
        {"error": message},
        status_code,
    )


@app.route("/", methods=["GET"])
def index():
    return make_response(
        {
            "message": "Welcome to the Workout Tracker API",
        },
        200,
    )


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()

    return make_response(
        workouts_schema.dump(workouts),
        200,
    )


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return json_error("Workout not found.", 404)

    return make_response(
        workout_schema.dump(workout),
        200,
    )


@app.route("/workouts", methods=["POST"])
def create_workout():
    json_data = request.get_json(silent=True)

    if json_data is None:
        return json_error(
            "Request body must contain valid JSON.",
            400,
        )

    try:
        validated_data = workout_schema.load(json_data)
        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return make_response(
            workout_schema.dump(workout),
            201,
        )

    except ValidationError as error:
        return make_response(
            {"errors": error.messages},
            400,
        )

    except ValueError as error:
        db.session.rollback()
        return json_error(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return json_error(
            "Workout could not be created.",
            400,
        )


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return json_error("Workout not found.", 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response("", 204)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()

    return make_response(
        exercises_schema.dump(exercises),
        200,
    )


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return json_error("Exercise not found.", 404)

    return make_response(
        exercise_schema.dump(exercise),
        200,
    )


@app.route("/exercises", methods=["POST"])
def create_exercise():
    json_data = request.get_json(silent=True)

    if json_data is None:
        return json_error(
            "Request body must contain valid JSON.",
            400,
        )

    try:
        validated_data = exercise_schema.load(json_data)
        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return make_response(
            exercise_schema.dump(exercise),
            201,
        )

    except ValidationError as error:
        return make_response(
            {"errors": error.messages},
            400,
        )

    except ValueError as error:
        db.session.rollback()
        return json_error(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return json_error(
            "An exercise with that name already exists.",
            409,
        )


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return json_error("Exercise not found.", 404)

    db.session.delete(exercise)
    db.session.commit()

    return make_response("", 204)


@app.route(
    "/workouts/<int:workout_id>"
    "/exercises/<int:exercise_id>"
    "/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return json_error("Workout not found.", 404)

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return json_error("Exercise not found.", 404)

    json_data = request.get_json(silent=True)

    if json_data is None:
        return json_error(
            "Request body must contain valid JSON.",
            400,
        )

    try:
        validated_data = workout_exercise_schema.load(
            json_data
        )

        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            **validated_data,
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(
            workout_exercise_schema.dump(
                workout_exercise
            ),
            201,
        )

    except ValidationError as error:
        return make_response(
            {"errors": error.messages},
            400,
        )

    except ValueError as error:
        db.session.rollback()
        return json_error(str(error), 400)

    except IntegrityError:
        db.session.rollback()
        return json_error(
            "This exercise is already attached to this workout.",
            409,
        )


if __name__ == "__main__":
    app.run(port=5555, debug=True)