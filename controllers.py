from fastapi import Request, HTTPException
from models import *
from schemas import *
from datetime import datetime, timedelta
from helpers import get_weeks_in_month
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
    :rtype: list[]
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
            user=user, **workout_session.model_dump(exclude_none=True)
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
    :rtype: list[]
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


async def create_user_exercise_log(
    id: int, user: User, exercise_log: ExerciseLogCreate
) -> ExerciseLogBase:
    """
    Create a new exercise log for a user.
    :param id: The ID of the workout session for which the log belongs or refers
    :param user: The user for whom the exercise log is created.
    :type user: User
    :param exercise_log: The exercise log data to create.
    :type exercise_log: ExerciseLog_Pydantic
    :raises HTTPException: If there is an error creating the exercise log.
    :return: The created exercise log.
    :rtype: ExerciseLog
    """
    try:
        # Create the exercise log
        exercise_log_obj = await ExerciseLog.create(
            workout_session_id=id,
            **exercise_log.model_dump(),
        )
        # Retrieve or create the exercise summary
        exercise_summary_obj, created = await ExerciseSummary.get_or_create(
            exercise_log=exercise_log_obj,
            defaults={
                "total_sets": exercise_log.sets,
                "total_reps": exercise_log.reps,
                "total_holds": exercise_log.reps,
            },
        )

        if not created:
            # update the existing summary
            exercise_summary_obj.sets += exercise_log.sets
            exercise_summary_obj.reps += exercise_log.reps
            await exercise_summary_obj.save()

        return exercise_log_obj

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create exercise log: {e}"
        )


async def update_user_exercise_log(
    id: int, user: User, exercise: ExerciseLogUpdate
) -> ExerciseLogBase:
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


async def get_user_exercise_summary(id: int, user: User) -> ExerciseSummaryBase:
    """
    Retrieve a specific exercise summary for a user's exercise log.

    :param id: The ID of the exercise log.
    :type id: int
    :param user: The user for whom the exercise summary is retrieved.
    :type user: User
    :raises HTTPException: If the exercise summary does not exist or there is an error retrieving it.
    :return: The exercise summary.
    :rtype: ExerciseSummary
    """
    try:
        exercise_summary_obj = await ExerciseSummary.get(
            exercise_log_id=id, exercise_log__workout_session__user=user
        )
        return exercise_summary_obj
    except DoesNotExist:
        raise HTTPException(
            status_code=404, details=f"Failed to retrieve exercise summary: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve exercise summary: {e}"
        )


async def create_user_exercise_summary(
    id: int, summary: ExerciseSummaryCreate
) -> ExerciseSummaryCreate:
    """
    Create a new exercise summary for a user's exercise log.

    :param id: The ID of the exercise log.
    :type id: int
    :param summary: The exercise summary data to be created.
    :type summary: ExerciseSummaryCreate
    :raises HTTPException: If there is an error creating the exercise summary.
    :return: The created exercise summary.
    :rtype: ExerciseSummary
    """
    try:
        exercise_summary_obj = await ExerciseSummary.create(
            exercise_log_id=id, **summary.model_dump()
        )
        return exercise_summary_obj
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Failed to create exercise summary: {e}"
        )


async def update_user_exercise_summary(
    id: int, user: User, summary: ExerciseSummaryUpdate
) -> ExerciseSummaryUpdate:
    """
    Update an existing exercise summary for a user's exercise log.

    :param id: The ID of the exercise summary to update.
    :type id: int
    :param user: The user who owns the exercise log.
    :type user: User
    :param summary: The updated exercise summary data.
    :type summary: ExerciseSummaryUpdate
    :raises HTTPException: If the exercise summary is not found or there is an error updating it.
    :return: The updated exercise summary.
    :rtype: ExerciseSummary
    """
    try:
        exercise_summary_obj = await ExerciseSummary.get(
            id=id, exercise_log__workout_session__user=user
        )
        exercise_summary = await exercise_summary_obj.update_from_dict(
            summary.model_dump(exclude_none=True)
        )
        await exercise_summary.save()
        return exercise_summary
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Exercise summary not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update exercise summary: {e}"
        )


async def delete_user_exercise_summary(id: int, user: User) -> None:
    """
    Delete an existing exercise summary for a user's exercise log.

    :param id: The ID of the exercise summary to delete.
    :type id: int
    :param user: The user who owns the exercise log.
    :type user: User
    :raises HTTPException: If the exercise summary is not found or there is an error deleting it.
    :return: None
    """
    try:
        exercise_summary_obj = await ExerciseSummary.get(id=id, user=user)
        await exercise_summary_obj.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Exercise summary not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete exercise summary: {e}"
        )


async def get_user_exercises(user: User) -> list[ExerciseBase]:
    """
    Retrieve all exercises for a user.

    :param user: The user whose exercises are to be retrieved.
    :type user: User
    :raises HTTPException: If there is an error retrieving the exercises.
    :return: A list of exercises.
    :rtype: list[ExerciseBase]
    """
    try:
        exercises = Exercise.filter(user=user)
        return await Exercise_Pydantic_List.from_queryset(exercises)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve exercises: {e}"
        )


async def get_user_exercise(id: int, user: User) -> ExerciseBase:
    """
    Retrieve a specific exercise for a user.

    :param id: The ID of the exercise to retrieve.
    :type id: int
    :param user: The user whose exercise is to be retrieved.
    :type user: User
    :raises HTTPException: If there is an error retrieving the exercise.
    :return: The retrieved exercise.
    :rtype: ExerciseBase
    """
    try:
        exercise_obj = await Exercise.get(id=id, user=user)
        return exercise_obj
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Exercise not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve exercise: {e}")


async def create_user_exercise(user: User, exercise: ExerciseCreate) -> ExerciseBase:
    """
    Create a new exercise for a user.

    :param user: The user for whom the exercise is created.
    :type user: User
    :param exercise: The exercise data to create.
    :type exercise: ExerciseCreate
    :raises HTTPException: If there is an error creating the exercise.
    :return: The created exercise.
    :rtype: ExerciseBase
    """
    try:
        exercise_obj = await Exercise.create(user=user, **exercise.model_dump())
        return exercise_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create exercise: {e}")


async def update_user_exercise(
    id: int, user: User, exercise: ExerciseUpdate
) -> ExerciseBase:
    """
    Update an existing exercise for a user.

    :param id: The ID of the exercise to update.
    :type id: int
    :param user: The user for whom the exercise is updated.
    :type user: User
    :param exercise: The updated exercise data.
    :type exercise: ExerciseUpdate
    :raises HTTPException: If there is an error updating the exercise.
    :return: The updated exercise.
    :rtype: ExerciseBase
    """
    try:
        exercise_obj = await Exercise.get(id=id, user=user)
        exercise_ = await exercise_obj.update_from_dict(
            exercise.model_dump(exclude_none=True)
        )
        await exercise_.save()
        return exercise_
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Exercise not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update exercise: {e}")


async def delete_user_exercise(id: int, user: User) -> None:
    """
    Delete an existing exercise for a user.

    :param id: The ID of the exercise to delete.
    :type id: int
    :param user: The user for whom the exercise is deleted.
    :type user: User
    :raises HTTPException: If there is an error deleting the exercise.
    :return: None
    """
    try:
        exercise_obj = await Exercise.get(id=id, user=user)
        await exercise_obj.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Exercise not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete exercise: {e}")


async def get_weekly_exercise_summary(user: User, week_start: datetime) -> dict:
    """
    Get the exercise summary for a user for the entire week.

    :param user: The user for whom the exercise summary is calculated.
    :type user: User
    :param week_start: The start date of the week.
    :type week_start: datetime
    :return: A dictionary containing the total sets and reps for the week.
    :rtype: dict
    """
    try:
        # Calculate the end date of the week
        week_end = week_start + timedelta(days=7)

        # Fetch all exercise logs for the user within the week
        exercise_logs = await ExerciseLog.filter(
            workout_session__user=user,
            workout_session__date__gte=week_start,
            workout_session__date__lt=week_end,
        )

        # Aggregate the sets and reps
        total_sets = sum(log.sets for log in exercise_logs)
        total_reps = sum(log.reps for log in exercise_logs)
        total_holds = sum(log.reps for log in exercise_logs)

        return {
            "total_sets": total_sets,
            "total_reps": total_reps,
            "total_holds": total_holds,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate weekly exercise summary: {e}"
        )


async def get_monthly_exercise_summary(user: User, year: int, month: int) -> list:
    """
    Get the exercise summary for a user for each week in a given month.

    :param user: The user for whom the exercise summary is calculated.
    :type user: User
    :param year: The year of the month.
    :type year: int
    :param month: The month for which to get the exercise summary.
    :type month: int
    :return: A list of dictionaries containing the total sets and reps for each week.
    :rtype: list
    """
    try:
        weeks = get_weeks_in_month(year, month)
        weekly_summaries = [
            {
                "week_start": week_start,
                "week_end": week_end,
                "summary": await get_weekly_exercise_summary(user, week_start),
            }
            for week_start, week_end in weeks
        ]

        return weekly_summaries

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate monthly exercise summary: {e}"
        )
