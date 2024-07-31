import uvicorn
from database import TORTOISE_ORM, TORTOISE_ORM_TEST
from fastapi import FastAPI, HTTPException, Security, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import B2CMultiTenantAuthorizationCodeBearer, user
from tortoise.contrib.fastapi import RegisterTortoise
from tortoise import Tortoise
from models import *
from schemas import *
from settings import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from controllers import *


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Load OpenID config on startup and Registers Tortoise-ORM with set-up and tear-down inside a FastAPI application\'ss lifespan.
    :raises:Any exceptions raised by `azure_scheme.openid_config.load_config()`
    :return: None

    """
    if getattr(app.state, "testing", False):
        # If we're in unit tests, create a DB with a dynamic name (the {} placeholder), create schemas and drop
        # the database when the app's lifespan ends
        # reference: https://github.com/tortoise/tortoise-orm/issues/1676#issuecomment-2239073869
        async with RegisterTortoise(
            app=app,
            config=TORTOISE_ORM_TEST,
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield

    else:
        await azure_scheme.openid_config.load_config()
        async with RegisterTortoise(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield


app = FastAPI(
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": settings.OPENAPI_CLIENT_ID,
        "scopes": settings.SCOPE_NAME,
    },
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

azure_scheme = B2CMultiTenantAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    openid_config_url=settings.OPENID_CONFIG_URL,
    openapi_authorization_url=settings.OPENAPI_AUTHORIZATION_URL,
    openapi_token_url=settings.OPENAPI_TOKEN_URL,
    scopes=settings.SCOPES,
    validate_iss=False,
)


def main():
    uvicorn.run("project:app", reload=True)


@app.get(
    "/workout-plans",
    response_model=WorkoutPlan_Pydantic_List,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_plans(request: Request):
    """
    Retrieve workout plans for the authenticated user.

    Args:
        request (Request): The incoming request object.

    Returns:
        list: A list of workout plans in the response model format.

    Raises:
        HTTPException: If the user is unauthorized or if there is an error retrieving the workout plans.
    """
    user = await get_authenticated_user(request)
    return await get_user_workout_plans(user)


@app.get(
    "/workout-plan/{id}",
    response_model=WorkoutPlan_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_plan(request: Request, id: int):
    """
    Retrieve a workout plan by its ID.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout plan to retrieve.

    Returns:
        WorkoutPlan_Pydantic: The retrieved workout plan.

    Raises:
        HTTPException: If the workout plan with the given ID does not exist.
    """
    user = await get_authenticated_user(request)
    return await get_user_workout_plan(id, user)


@app.post(
    "/workout-plans",
    response_model=WorkoutPlan_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def create_workout_plan(request: Request, workout_plan: WorkoutPlanCreate):
    """
    Create a new workout plan for the authenticated user.

    Args:
        request (Request): The incoming request object.
        workout_plan (WorkoutPlanCreate): The workout plan data to be created.

    Returns:
        WorkoutPlan_Pydantic: The created workout plan.

    Raises:
        HTTPException: If there is an error creating the workout plan.
    """
    user = await get_authenticated_user(request)
    return await create_user_workout_plan(user, workout_plan)


@app.patch(
    "/workout-plan/{id}",
    response_model=WorkoutPlan_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def update_workout_plan(
    request: Request, id: int, workout_plan: WorkoutPlanUpdate
):
    """
    Update a workout plan for a specific ID.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout plan to be updated.
        workout_plan (WorkoutPlanUpdate): The updated workout plan data.

    Returns:
        WorkoutPlan_Pydantic: The updated workout plan.

    Raises:
        HTTPException: If there is an error updating the workout plan.
    """
    user = await get_authenticated_user(request)
    return await update_user_workout_plan(id, user, workout_plan)


@app.delete("/workout-plan/{id}", dependencies=[Security(azure_scheme)])
async def delete_workout_plan(request: Request, id: int) -> None:
    """
    Delete a workout plan for a specific ID.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout plan to be deleted.

    Returns:
        None: This function does not return any data.

    Raises:
        HTTPException: If there is an error deleting the workout plan.
    """
    user = await get_authenticated_user(request)
    await delete_user_workout_plan(id, user)
    return Response(status_code=204)


@app.get(
    "/workout-sessions",
    response_model=WorkoutSession_Pydantic_List,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_sessions(request: Request):
    """
    Retrieve all workout sessions for the authenticated user.

    Args:
        request (Request): The incoming request object.

    Returns:
        WorkoutSession_Pydantic_List: A list of workout sessions for the user.

    Raises:
        HTTPException: If there is an error retrieving the workout sessions.
    """
    user = await get_authenticated_user(request)
    return await get_user_workout_sessions(user)


@app.get(
    "/workout-session/{id}",
    response_model=WorkoutSession_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_session(request: Request, id: int):
    """
    Retrieve a specific workout session for the authenticated user by ID.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout session to retrieve.

    Returns:
        WorkoutSession_Pydantic: The workout session for the user.

    Raises:
        HTTPException: If there is an error retrieving the workout session.
    """
    user = await get_authenticated_user(request)
    return await get_user_workout_session(id, user)


@app.post(
    "/workout-sessions",
    response_model=WorkoutSession_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def create_workout_session(
    request: Request, workout_session: WorkoutSessionCreate
):
    """
    Create a new workout session for the authenticated user.

    Args:
        request (Request): The incoming request object.
        workout_session (WorkoutSessionCreate): The workout session data to create.

    Returns:
        WorkoutSession_Pydantic: The created workout session.

    Raises:
        HTTPException: If there is an error creating the workout session.
    """
    user = await get_authenticated_user(request)
    return await create_user_workout_session(user, workout_session)


@app.patch(
    "/workout-session/{id}",
    response_model=WorkoutSession_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def update_workout_session(
    request: Request, id: int, workout_session: WorkoutSessionUpdate
):
    """
    Update an existing workout session for the authenticated user.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout session to update.
        workout_session (WorkoutSessionUpdate): The updated workout session data.

    Returns:
        WorkoutSession_Pydantic: The updated workout session.

    Raises:
        HTTPException: If there is an error updating the workout session.
    """
    user = await get_authenticated_user(request)
    return await update_user_workout_session(id, user, workout_session)


@app.delete(
    "/workout-session/{id}",
    dependencies=[Security(azure_scheme)],
)
async def delete_workout_session(request: Request, id: int) -> None:
    """
    Delete an existing workout session for the authenticated user.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout session to delete.

    Returns:
        None

    Raises:
        HTTPException: If there is an error deleting the workout session.
    """
    user = await get_authenticated_user(request)
    await delete_user_workout_session(id, user)
    return Response(status_code=204)


@app.get(
    "/exercise-logs/workout-session/{id}",
    response_model=ExerciseLog_Pydantic_List,
    dependencies=[Security(azure_scheme)],
)
async def get_exercise_logs(request: Request, id: int):
    user = await get_authenticated_user(request)
    return await get_user_exercise_logs(id, user)


@app.get(
    "/exercise-log/{id}/workout-session",
    response_model=ExerciseLog_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def get_exercise_log(request: Request, id: int):
    user = await get_authenticated_user(request)
    return await get_user_exercise_log(id, user)


@app.post(
    "/exercise-logs/workout-session/{id}",
    response_model=ExerciseLog_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def create_exercise_log(
    request: Request, id: int, exercise_log: ExerciseLogCreate
):
    return await create_user_exercise_log(id, exercise_log)


@app.patch(
    "/exercise-log/{id}/workout-session",
    response_model=ExerciseLog_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def update_exercise_log(
    request: Request, id: int, exercise_log: ExerciseLogUpdate
):
    user = await get_authenticated_user(request)
    return await update_user_exercise_log(id, user, exercise_log)


@app.delete("/exercise-log/{id}/workout-session", dependencies=[Security(azure_scheme)])
async def delete_exercise_log(request: Request, id: int) -> None:

    user = await get_authenticated_user(request)
    await delete_user_exercise_log(id, user)
    return Response(status_code=204)


if __name__ == "__main__":
    main()
