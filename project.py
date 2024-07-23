import uvicorn
from database import TORTOISE_ORM
from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import B2CMultiTenantAuthorizationCodeBearer, user
from tortoise.contrib.pydantic import pydantic_queryset_creator
from tortoise.contrib.fastapi import register_tortoise
from models import *
from schemas import *
from settings import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Load OpenID config on startup.

    This function is an async context manager that loads the OpenID config
    when the application starts up. It uses the `azure_scheme.openid_config.load_config()`
    function to load the config. The config is loaded before the context is entered,
    and it is unloaded after the context is exited.

    Usage:
    ```
    async with lifespan(app):
        # Code that requires the OpenID config
    ```

    Returns:
    None

    Raises:
    Any exceptions raised by `azure_scheme.openid_config.load_config()`
    """
    await azure_scheme.openid_config.load_config()
    yield


app = FastAPI(
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": settings.OPENAPI_CLIENT_ID,
        "scopes": settings.SCOPE_NAME,
    },
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

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


def main():
    uvicorn.run("project:app", reload=True)


@app.get(
    "/workout-plans",
    response_model=WorkoutPlan_Pydantic_List,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_plans(request: Request) -> list:
    user_dict = request.state.user.dict()
    if not user_dict:
        raise HTTPException(status_code=401, detail="Unauthorized User")
    user = await User.get_or_create(object_id=user_dict["sub"])

    try:
        workout_plans = WorkoutPlan.filter(user=user)
        return await WorkoutPlan_Pydantic_List.from_queryset(workout_plans)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Failed to retrieve workout plans: {e}")

if __name__ == "__main__":
    main()
