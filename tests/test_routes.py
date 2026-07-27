import pytest

from server.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"]


def test_get_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_exercises(client):
    response = client.get("/exercises")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_missing_workout_returns_404(client):
    response = client.get("/workouts/99999")

    assert response.status_code == 404


def test_missing_exercise_returns_404(client):
    response = client.get("/exercises/99999")

    assert response.status_code == 404


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-07-26",
            "duration_minutes": 45,
            "notes": "Test workout",
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["duration_minutes"] == 45


def test_invalid_workout_returns_400(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-07-26",
            "duration_minutes": 0,
            "notes": "Invalid workout",
        },
    )

    assert response.status_code == 400