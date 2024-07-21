import bcrypt
from tortoise import fields, models
from validators import email
from helpers import validate_non_negative
MAXLENGTH = 50


class User(models.Model):
    username = fields.CharField(max_length=MAXLENGTH, unique=True)
    password = fields.CharField(max_length=MAXLENGTH, default="misc")  # Renamed from _password
    email = fields.CharField(max_length=MAXLENGTH)
    created_at = fields.DatetimeField(auto_now_add=True)

    class PydanticMeta:
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super().__init__(*args, **kwargs)
        if password:
            self.set_password(password)  # Use a method to hash and set the password

    @staticmethod
    def validate_email(s):
        if email(s):
            return True
        else:
            return False

    async def save(self, *args, **kwargs):
        if not self.validate_email(self.email):
            raise ValueError("Invalid email")
        await super().save(*args, **kwargs)

    def set_password(self, password):
        # Hash password and set it
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 

        
    

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
