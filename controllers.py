from typing import Coroutine
from fastapi import Request, HTTPException
from models import *
from schemas import *


from tortoise.exceptions import DoesNotExist


async def get_authenticated_user(request: Request) -> User:
    """
    Extract and validate the authenticated user from the request.

    Args:
        request (Request): The incoming request object.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user is unauthorized.
    """
    user_dict = request.state.user.model_dump()
    if not user_dict:
        raise HTTPException(status_code=401, detail="Unauthorized User")
    user, _ = await User.get_or_create(object_id=user_dict["sub"])
    return user


async def get_user_workout_plans(user: User) -> list[WorkoutPlanBase]:
    """
    Retrieve workout plans for a user.

    :param user: The user for whom the workout plans are retrieved.
    :return: A list of workout plans in the response model format.
    :raises HTTPException: If there is an error retrieving the workout plans.
    :rtype: []
    """
    try:
        workout_plans = WorkoutPlan.filter(user=user)
        return await WorkoutPlan_Pydantic_List.from_queryset(workout_plans)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve workout plans: {e}"
        )


async def get_user_workout_plan(id: int, user: User) -> WorkoutPlan:
    """
    Retrieve a specific workout plan for a user.

    :param user: The user for whom the workout plan is retrieved.
    :param workout_id: The ID of the workout plan to retrieve.
    :raises HTTPException: If there is an error retrieving the workout plan.
    :return: The retrieved workout plan.
    :rtype: WorkoutPlan
    """

    try:
        workout_plan_obj = await WorkoutPlan.get(id=id, user=user)
        return workout_plan_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Workout Plan not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve workout plan: {e}"
        )


async def create_user_workout_plan(
    user: User, workout: WorkoutPlanCreate
) -> WorkoutPlan:
    """
    Create a workout plan for a user.

    :param user: The user for whom the workout plan is created.
    :param workout: The details of the workout plan.
    :raises HTTPException: If there is an error creating the workout plan.
    :return: The created workout plan.
    :rtype: WorkoutPlan
    """
    try:
        workout_plan_obj = await WorkoutPlan.create(user=user, **workout.model_dump())
        return workout_plan_obj
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create workout plan: {e}"
        )


async def update_user_workout_plan(
    id: int, user: User, workout: WorkoutPlanUpdate
) -> WorkoutPlan:
    """
    Update a workout plan for a user.

    :param user: The user for whom the workout plan is updated.
    :param workout: The details of the workout plan.
    :raises HTTPException: If there is an error updating the workout plan.
    :return: The updated workout plan.
    :rtype: WorkoutPlan
    """
    try:
        workout_plan_obj = await WorkoutPlan.get(id=id, user=user)
        workout_plan = await workout_plan_obj.update_from_dict(
            workout.model_dump(exclude_none=True)
        )
        await workout_plan.save()
        return workout_plan
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Workout plan not found ")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update workout plan: {e}"
        )


async def delete_user_workout_plan(id: int, user: User) -> None:
    """
    Deletes a workout plan for a user.

    :param id: The ID of the workout plan to be deleted.
    :param user: The user for whom the workout plan is deleted.
    :raises HTTPException: If there is an error deleting the workout plan.
    :return: None
    """
    try:
        workout_plan_obj = await WorkoutPlan.get(id=id, user=user)
        await workout_plan_obj.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Workout plan does not exist")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete workout plan: {e}"
        )


async def get_user_workout_sessions(user: User) -> list[WorkoutSessionBase]:
    """
    Retrieves all workout sessions for a user.

    :param user: The user for whom the workout sessions are retrieved.
    :raises HTTPException: If there is an error retrieving the workout sessions.
    :return: A list of workout sessions for the user.
    :rtype: list
    """
    try:
        workout_sessions = WorkoutSession.filter(user=user)
        return await WorkoutSession_Pydantic_List.from_queryset(workout_sessions)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve workout sessions: {e}"
        )


async def get_user_workout_session(id: int, user: User) -> WorkoutSessionBase:
    """
    Retrieve a specific workout session for a user.

    :param id: The ID of the workout session to retrieve.
    :type id: int
    :param user: The user for whom the workout session is retrieved.
    :type user: User
    :raises HTTPException: If there is an error retrieving the workout session.
    :return: The workout session object.
    :rtype: WorkoutSession
    """
    try:
        workout_sesssion_obj = await WorkoutSession.get(id=id, user=user)
        return workout_sesssion_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Workout Session not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve workout session: {e}"
        )


async def create_user_workout_session(
    user: User, workout_session: WorkoutSessionCreate
) -> WorkoutSessionBase:
    """
    Create a new workout session for a user.

    :param user: The user for whom the workout session is created.
    :type user: User
    :param workout_session: The workout session data to create.
    :type workout_session: dict
    :raises HTTPException: If there is an error creating the workout session.
    :return: The created workout session object.
    :rtype: WorkoutSession
    """
    try:
        workout_session_obj = await WorkoutSession.create(
            user=user, **workout_session.model_dump()
        )
        return workout_session_obj
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create workout session: {e}"
        )


async def update_user_workout_session(
    id: int, user: User, workout: WorkoutSessionUpdate
) -> WorkoutSessionBase:
    """
    Update an existing workout session for a user.

    :param id: The ID of the workout session to update.
    :type id: int
    :param user: The user for whom the workout session is updated.
    :type user: User
    :param workout: The updated workout session data.
    :type workout: WorkoutSessionUpdate
    :raises HTTPException: If there is an error updating the workout session.
    :return: The updated workout session object.
    :rtype: WorkoutSession
    """
    try:
        workout_session_obj = await WorkoutSession.get(id=id, user=user)
        workout_session = await workout_session_obj.update_from_dict(
            workout.model_dump(exclude_none=True)
        )
        await workout_session.save()
        return workout_session
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Workout session not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update workout session: {e}"
        )


async def delete_user_workout_session(id: int, user: User) -> None:
    """
    Delete an existing workout session for a user.

    :param id: The ID of the workout session to delete.
    :type id: int
    :param user: The user for whom the workout session is deleted.
    :type user: User
    :raises HTTPException: If there is an error deleting the workout session.
    :return: None
    """
    try:
        workout_session_obj = await WorkoutSession.get(id=id, user=user)
        await workout_session_obj.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Workout session not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete workout session: {e}"
        )


async def get_user_exercise_logs(id: int, user: User) -> list[ExerciseLogBase]:
    """
    Retrieve all exercise logs for a user.
    :param id: The ID of the workout session for which the log belongs or refers
    :param user: The user for whom the exercise logs are retrieved.
    :type user: User
    :raises HTTPException: If there is an error retrieving the exercise logs.
    :return: A list of exercise logs for the user.
    :rtype: []
    """
    try:
        exercise_logs = await ExerciseLog.filter(
            workout_session__id=id, workout_session__user=user
        )
        return exercise_logs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve exercise logs: {e}"
        )


async def get_user_exercise_log(id: int, user: User) -> ExerciseLogBase:
    """
    Retrieve a specific exercise log for a user by ID.

    :param id: The ID of the exercise log to retrieve.
    :type id: int
    :raises HTTPException: If there is an error retrieving the exercise log.
    :return: The exercise log for the user.
    :rtype: ExerciseLog
    """
    try:
        exercise_log_obj = await ExerciseLog.get(id=id, workout_session__user=user)
        return exercise_log_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Exercise Log not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve exercise log: {e}"
        )


async def create_user_exercise_log(id: int, exercise_log: ExerciseLogCreate) -> ExerciseLogBase:  
    """
    Create a new exercise log for a user.
    :param id: The ID of the workout session for which the log belongs or refers
    :param user: The user for whom the exercise log is created.
    :type user: User
    :param exercise_log: The exercise log data to create.
    :type exercise_log: ExerciseLog_Pydantic
    :raises HTTPException: If there is an error creating the exercise log.
    :return: The created exercise log.
    :rtype: ExerciseLog_Pydantic
    """
    try:
        exercise_log_obj = await ExerciseLog.create(
            workout_session_id=id,
            **exercise_log.model_dump(),
        )
        return exercise_log_obj
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create exercise log: {e}"
        )


async def update_user_exercise_log(id: int, user: User, exercise: ExerciseLogUpdate) -> ExerciseLogBase:  
    """
    Update an existing exercise log for a user.

    :param id: The ID of the exercise log to update.
    :type id: int
    :param user: The user for whom the exercise log is updated.
    :type user: User
    :param exercise: The updated exercise log data.
    :type exercise: ExerciseLog_Pydantic
    :raises HTTPException: If there is an error updating the exercise log.
    :return: The updated exercise log.
    :rtype: ExerciseLog
    """
    try:
        exercise_log_obj = await ExerciseLog.get(id=id, workout_session__user=user)
        exercise_log = await exercise_log_obj.update_from_dict(
            exercise.model_dump(exclude_none=True)
        )
        await exercise_log.save()
        return exercise_log
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Exercise log not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update exercise log: {e}"
        )


async def delete_user_exercise_log(id: int, user: User) -> None:
    """
    Delete an existing exercise log for a user.

    :param id: The ID of the exercise log to delete.
    :type id: int
    :param user: The user for whom the exercise log is deleted.
    :type user: User
    :raises HTTPException: If there is an error deleting the exercise log.
    :return: None
    """
    try:
        exercise_log_obj = await ExerciseLog.get(id=id, workout_session__user=user)
        await exercise_log_obj.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Exercise log not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete exercise log: {e}"
        )
