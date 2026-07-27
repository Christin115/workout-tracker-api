from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    workouts = association_proxy(
        "workout_exercises",
        "workout",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Exercise name must be a string.")

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Exercise name must contain at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Exercise name cannot exceed 100 characters."
            )

        return value

    @validates("category")
    def validate_category(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Exercise category must be a string.")

        value = value.strip().lower()

        if len(value) < 2:
            raise ValueError(
                "Exercise category must contain at least 2 characters."
            )

        if len(value) > 50:
            raise ValueError(
                "Exercise category cannot exceed 50 characters."
            )

        return value

    @validates("equipment_needed")
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError(
                "equipment_needed must be true or false."
            )

        return value

    def __repr__(self):
        return (
            f"<Exercise id={self.id}, "
            f"name={self.name!r}, "
            f"category={self.category!r}>"
        )


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(
        db.Integer,
        nullable=False,
    )
    notes = db.Column(db.Text, nullable=True)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    exercises = association_proxy(
        "workout_exercises",
        "exercise",
    )

    __table_args__ = (
        db.CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive",
        ),
    )

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(
                "Workout duration must be an integer."
            )

        if value <= 0:
            raise ValueError(
                "Workout duration must be greater than zero."
            )

        if value > 1440:
            raise ValueError(
                "Workout duration cannot exceed 1440 minutes."
            )

        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("Workout notes must be a string.")

        value = value.strip()

        if len(value) > 1000:
            raise ValueError(
                "Workout notes cannot exceed 1000 characters."
            )

        return value

    def __repr__(self):
        return (
            f"<Workout id={self.id}, "
            f"date={self.date}, "
            f"duration_minutes={self.duration_minutes}>"
        )


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False,
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False,
    )

    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(
        db.Integer,
        nullable=True,
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises",
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises",
    )

    __table_args__ = (
        db.CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_reps_positive",
        ),
        db.CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="check_sets_positive",
        ),
        db.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="check_duration_seconds_positive",
        ),
        db.UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_exercise_per_workout",
        ),
    )

    @validates("reps", "sets", "duration_seconds")
    def validate_positive_integer(self, key, value):
        if value is None:
            return value

        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{key} must be an integer.")

        if value <= 0:
            raise ValueError(
                f"{key} must be greater than zero."
            )

        return value

    def __repr__(self):
        return (
            f"<WorkoutExercise id={self.id}, "
            f"workout_id={self.workout_id}, "
            f"exercise_id={self.exercise_id}>"
        )