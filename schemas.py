from tortoise.contrib.pydantic import pydantic_model_creator
from models import *

User_Pydantic = pydantic_model_creator(User)
WorkoutPlan_Pydantic = pydantic_model_creator(WorkoutPlan)
WorkoutSession_Pydantic = pydantic_model_creator(WorkoutSession)
ExerciseLog_Pydantic = pydantic_model_creator(ExerciseLog)
ExerciseSummary_Pydantic = pydantic_model_creator(ExerciseSummary)
ExerciseLog_Pydantic = pydantic_model_creator(Exercise)
CalendarEntry_Pydantic = pydantic_model_creator(CalendarEntry)
