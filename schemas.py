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

Exercise_Pydantic = pydantic_model_creator(Exercise)
Exercise_Pydantic_List = pydantic_queryset_creator(Exercise)

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

class ExerciseLogBase(BaseModel):
    exercise_id: int # required to pass an id in request body to reference which exercise to
    sets: int
    reps: int
    intensity: int
    exertion_scale: int

class ExerciseLogCreate(ExerciseLogBase):
    ...

class ExerciseLogUpdate(BaseModel):
    exercise_id: int  # required to pass an id in request body to reference which exercise to
    sets: Optional[int] = None
    reps: Optional[int] = None
    intensity: Optional[int] = None
    exertion_scale: Optional[int] = None

class ExerciseBase(BaseModel):
    name: str
    description: str
    category: str
    muscle_group: str

class ExerciseCreate(ExerciseBase):
    ...

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    muscle_group: Optional[str] = None