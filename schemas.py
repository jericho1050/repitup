import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from models import *

User_Pydantic = pydantic_model_creator(User)
WorkoutPlan_Pydantic = pydantic_model_creator(WorkoutPlan)
WorkoutSession_Pydantic = pydantic_model_creator(WorkoutSession)
ExerciseLog_Pydantic = pydantic_model_creator(ExerciseLog)
ExerciseSummary_Pydantic = pydantic_model_creator(ExerciseSummary)
ExerciseLog_Pydantic = pydantic_model_creator(Exercise)
CalendarEntry_Pydantic = pydantic_model_creator(CalendarEntry)


class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserIn_2(BaseModel):
    username: str
    password: str