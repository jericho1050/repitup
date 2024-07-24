from typing import Coroutine
from fastapi import HTTPException

from models import *
from schemas import *

async def get_user_workout_plans(user: User) -> list:
    """
    Retrieve workout plans for a user.

    :param user: The user for whom the workout plans are retrieved.
    :return: A list of workout plans in the response model format.
    :raises HTTPException: If there is an error retrieving the workout plans.
    """
    try:
        workout_plans = WorkoutPlan.filter(user=user)
        return await WorkoutPlan_Pydantic_List.from_queryset(workout_plans)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve workout plans: {e}")


async def get_user_workout_plan(id: int) -> WorkoutPlan:
    """
    Retrieve a specific workout plan for a user.

    :param user: The user for whom the workout plan is retrieved.
    :param workout_id: The ID of the workout plan to retrieve.
    :raises HTTPException: If there is an error retrieving the workout plan.
    :return: The retrieved workout plan.
    :rtype: class
    """

    try:
        workout_plan = await WorkoutPlan.get(id=id)
        return workout_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve workout plan: {e}")


async def create_user_workout_plan(user: User, workout: WorkoutPlanCreate) -> WorkoutPlan:
    """
    Create a workout plan for a user.

    :param user: The user for whom the workout plan is created.
    :param workout: The details of the workout plan.
    :raises HTTPException: If there is an error creating the workout plan.
    :return: The created workout plan.
    :rtype: class
    """
    try:
        workout_plan = await WorkoutPlan.create(user=user, **workout.model_dump())
        return workout_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workout plan: {e}")
    

async def update_user_workout_plan(id: int, user: User, workout: WorkoutPlanUpdate) -> WorkoutPlan:
    """
    Update a workout plan for a user.

    :param user: The user for whom the workout plan is updated.
    :param workout: The details of the workout plan.
    :raises HTTPException: If there is an error updating the workout plan.
    :return: The updated workout plan.
    :rtype: class
    """
    try:
        workout_plan_obj = await WorkoutPlan.get(id=id, user=user)
        workout_plan = await workout_plan_obj.update_from_dict(workout.model_dump(exclude_none=True))
        return workout_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update workout plan: {e}")
    
async def delete_user_workout_plan(id: int, user: User) -> None:
    """
    Deletes a workout plan for a user.

    :param user: The user for whom the workout plan is deleted.
    :raises HTTPException: If there is an error deleting the workout plan.
    :return: None
    """
    try:
        workout_plan_obj = await WorkoutPlan.get(id=id, user=user)
        await workout_plan_obj.delete()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete workout plan: {e}")
