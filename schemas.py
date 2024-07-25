from datetime import datetime
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel
from models import *

User_Pydantic = pydantic_model_creator(User)

WorkoutPlan_Pydantic = pydantic_model_creator(WorkoutPlan)
WorkoutPlan_Pydantic_List = pydantic_queryset_creator(WorkoutPlan)

WorkoutSession_Pydantic = pydantic_model_creator(WorkoutSession)
WorkoutSession_Pydantic_List = pydantic_queryset_creator(WorkoutSession)

ExerciseLog_Pydantic = pydantic_model_creator(ExerciseLog)
ExerciseLog_Pydantic_List = pydantic_queryset_creator(ExerciseLog)

ExerciseSummary_Pydantic = pydantic_model_creator(ExerciseSummary)
ExerciseSummary_Pydantic_List = pydantic_queryset_creator(ExerciseSummary)

ExerciseLog_Pydantic = pydantic_model_creator(Exercise)
ExerciseLog_Pydantic_List = pydantic_queryset_creator(Exercise)

CalendarEntry_Pydantic = pydantic_model_creator(CalendarEntry)


class WorkoutPlanBase(BaseModel):
    name: str
    description: str


class WorkoutPlanCreate(WorkoutPlanBase): ...


class WorkoutPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkoutSessionBase(BaseModel):
    date: datetime
    comments: str


class WorkoutSessionCreate(BaseModel):
    comments: str


class WorkoutSessionUpdate(BaseModel):
    date: Optional[datetime] = None
    comments: Optional[str] = None
