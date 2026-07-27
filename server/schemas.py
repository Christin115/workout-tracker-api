from marshmallow import Schema, fields, validate


class ExerciseSummarySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    category = fields.String(dump_only=True)
    equipment_needed = fields.Boolean(dump_only=True)


class WorkoutSummarySchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Integer(dump_only=True)
    notes = fields.String(
        dump_only=True,
        allow_none=True,
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)

    reps = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, max=1000),
    )

    sets = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, max=100),
    )

    duration_seconds = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, max=86400),
    )

    exercise = fields.Nested(
        ExerciseSummarySchema,
        dump_only=True,
    )

    workout = fields.Nested(
        WorkoutSummarySchema,
        dump_only=True,
    )


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=1440),
    )

    notes = fields.String(
        allow_none=True,
        load_default=None,
        validate=validate.Length(max=1000),
    )

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True,
    )


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )

    category = fields.String(
        required=True,
        validate=validate.Length(min=2, max=50),
    )

    equipment_needed = fields.Boolean(required=True)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True,
    )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
