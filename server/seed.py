#!/usr/bin/env python3

from datetime import date

from server.app import app
from server.models import Exercise, Workout, WorkoutExercise, db


with app.app_context():
    print("Clearing database...")
# Delete association records first to avoid foreign key constraint errors.

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    bench_press = Exercise(
        name="Bench Press",
        category="strength",
        equipment_needed=True,
    )

    push_ups = Exercise(
        name="Push Ups",
        category="strength",
        equipment_needed=False,
    )

    running = Exercise(
        name="Running",
        category="cardio",
        equipment_needed=False,
    )

    plank = Exercise(
        name="Plank",
        category="strength",
        equipment_needed=False,
    )

    yoga_stretch = Exercise(
        name="Yoga Stretch",
        category="flexibility",
        equipment_needed=False,
    )

    squats = Exercise(
        name="Barbell Squats",
        category="strength",
        equipment_needed=True,
    )

    db.session.add_all(
        [
            bench_press,
            push_ups,
            running,
            plank,
            yoga_stretch,
            squats,
        ]
    )

    print("Creating workouts...")

    upper_body_workout = Workout(
        date=date(2026, 7, 24),
        duration_minutes=60,
        notes="Upper-body strength session.",
    )

    cardio_workout = Workout(
        date=date(2026, 7, 25),
        duration_minutes=45,
        notes="Outdoor cardio and stretching.",
    )

    lower_body_workout = Workout(
        date=date(2026, 7, 26),
        duration_minutes=50,
        notes="Lower-body strength workout.",
    )

    db.session.add_all(
        [
            upper_body_workout,
            cardio_workout,
            lower_body_workout,
        ]
    )

    print("Creating workout exercise records...")

    db.session.add_all(
        [
            WorkoutExercise(
                workout=upper_body_workout,
                exercise=bench_press,
                sets=4,
                reps=8,
            ),
            WorkoutExercise(
                workout=upper_body_workout,
                exercise=push_ups,
                sets=3,
                reps=12,
            ),
            WorkoutExercise(
                workout=upper_body_workout,
                exercise=plank,
                sets=3,
                duration_seconds=60,
            ),
            WorkoutExercise(
                workout=cardio_workout,
                exercise=running,
                duration_seconds=1800,
            ),
            WorkoutExercise(
                workout=cardio_workout,
                exercise=yoga_stretch,
                duration_seconds=600,
            ),
            WorkoutExercise(
                workout=lower_body_workout,
                exercise=squats,
                sets=4,
                reps=10,
            ),
        ]
    )

    db.session.commit()

    print("Database seeded successfully.")