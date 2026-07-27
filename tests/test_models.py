import pytest

from server.app import app
from server.models import Exercise, Workout


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def test_exercise_rejects_empty_name(app_context):
    with pytest.raises(ValueError):
        Exercise(
            name="",
            category="Strength",
            equipment_needed="Barbell",
        )


def test_workout_rejects_zero_duration(app_context):
    with pytest.raises(ValueError):
        Workout(
            date="2026-07-26",
            duration_minutes=0,
            notes="Invalid workout",
        )


def test_valid_exercise(app_context):
    exercise = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=True,
    )

    assert exercise.name == "Squats"
    assert exercise.category == "strength"
    assert exercise.equipment_needed is True