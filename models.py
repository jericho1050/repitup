import bcrypt
from tortoise import fields, models
from validators import email
from helpers import validate_non_negative
MAXLENGTH = 50


class User(models.Model):
    object_id = fields.CharField(max_length=MAXLENGTH + 50, pk=True) # this will be used for querying Objects
    
    

class WorkoutPlan(models.Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=25)
    description = fields.TextField()


class WorkoutSession(models.Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    workout_plan = fields.ForeignKeyField("models.WorkoutPlan", on_delete=fields.CASCADE)
    date = fields.DatetimeField(auto_now=True)
    comments = fields.TextField()


class ExerciseLog(models.Model):
    workout_session = fields.ForeignKeyField("models.WorkoutSession", on_delete=fields.CASCADE)
    exercise = fields.ForeignKeyField("models.Exercise", on_delete=fields.CASCADE)
    sets = fields.IntField(validators=[validate_non_negative])
    reps = fields.IntField(validators=[validate_non_negative])
    intensity = fields.IntField(validators=[validate_non_negative])
    exertion_scale = fields.IntField(validators=[validate_non_negative])


class ExerciseSummary(models.Model):
    exercise = fields.ForeignKeyField("models.ExerciseLog")
    total_sets = fields.IntField(validators=[validate_non_negative])
    total_reps = fields.IntField(validators=[validate_non_negative])
    total_holds = fields.IntField(validators=[validate_non_negative])


class Exercise(models.Model):
    name = fields.CharField(max_length=MAXLENGTH)
    description = fields.TextField()
    category = fields.CharField(max_length=MAXLENGTH)
    muscle_group = fields.CharField(max_length=MAXLENGTH)


class CalendarEntry(models.Model):
    workout_session = fields.ForeignKeyField("models.WorkoutSession", on_delete=fields.CASCADE)
    date = fields.DatetimeField(auto_now=True)
