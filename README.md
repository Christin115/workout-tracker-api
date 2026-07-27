# Workout Tracker API

A Flask, SQLAlchemy, Flask-Migrate, SQLite, and Marshmallow backend for managing workouts, exercises, and the exercises assigned to each workout.

## Models

### Exercise

- `id`
- `name`
- `category`
- `equipment_needed`

### Workout

- `id`
- `date`
- `duration_minutes`
- `notes`

### WorkoutExercise

- `id`
- `workout_id`
- `exercise_id`
- `reps`
- `sets`
- `duration_seconds`

## Relationships

- A `WorkoutExercise` belongs to a `Workout`.
- A `WorkoutExercise` belongs to an `Exercise`.
- A `Workout` has many `WorkoutExercise` records.
- An `Exercise` has many `WorkoutExercise` records.
- A `Workout` has many exercises through `WorkoutExercise`.
- An `Exercise` has many workouts through `WorkoutExercise`.

## Installation with Pipenv

```bash
pipenv install
pipenv shell
cd server
```

## Installation with venv and pip

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd server
```

## Initialize the database

Run these commands from inside `server`:

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "Create workout application tables"
flask db upgrade head
```

If `migrations/` already exists, skip `flask db init`.

## Seed the database

```bash
python seed.py
```

## Run the API

```bash
python app.py
```

The API runs at:

```text
http://127.0.0.1:5555
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout and its exercise records |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise and its workout records |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example requests

### Create a workout

```bash
curl -X POST http://127.0.0.1:5555/workouts   -H "Content-Type: application/json"   -d '{
    "date": "2026-07-27",
    "duration_minutes": 45,
    "notes": "Evening workout"
  }'
```

### Create an exercise

```bash
curl -X POST http://127.0.0.1:5555/exercises   -H "Content-Type: application/json"   -d '{
    "name": "Jumping Jacks",
    "category": "cardio",
    "equipment_needed": false
  }'
```

### Add an exercise to a workout

```bash
curl -X POST   http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises   -H "Content-Type: application/json"   -d '{
    "sets": 4,
    "reps": 10
  }'
```

## Validation examples

The project includes multiple validations at every required level.

### Table constraints

- Required columns use `nullable=False`.
- Exercise names are unique.
- Workout duration must be positive.
- Sets, reps, and duration seconds must be positive when provided.
- The same exercise cannot be added twice to one workout.

### Model validations

- Exercise names and categories must be non-empty strings.
- Equipment required must be a Boolean.
- Workout duration must be a positive integer.
- Notes cannot exceed 1,000 characters.
- Sets, reps, and duration seconds must be positive integers.

### Schema validations

- Required fields are enforced.
- String lengths are checked.
- Integer ranges are checked.
- Date and Boolean values are deserialized and validated.
