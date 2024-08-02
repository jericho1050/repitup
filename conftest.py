import pytest
from httpx import AsyncClient, ASGITransport
from project import app as fastapi_app
from fastapi import Request
from fastapi_azure_auth.user import User
from project import azure_scheme
from tortoise.contrib.test import finalizer, initializer
import asgi_lifespan
from project import app


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    app.state.testing = True
    # db_url = "sqlite://:memory"  # Use in-memory SQLite for tests
    # initializer(["models"], db_url=db_url, app_label="models")
    # request.addfinalizer(finalizer)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def normal_user_client():
    async def mock_normal_user(request: Request):
        user = User(
            claims={},
            preferred_username="NormalUser",
            roles=[],
            aud="aud",
            tid="tid",
            access_token="123",
            is_guest=False,
            iat=1537231048,
            nbf=1537231048,
            exp=1537234948,
            iss="iss",
            aio="aio",
            sub="sub",
            oid="oid",
            uti="uti",
            rh="rh",
            ver="2.0",
        )
        request.state.user = user
        return user

    fastapi_app.dependency_overrides[azure_scheme] = mock_normal_user
    async with asgi_lifespan.LifespanManager(fastapi_app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture
async def created_workout_plan_id(normal_user_client):
    response = await normal_user_client.post(
        "/workout-plans",
        json={"name": "testing post method 1", "description": "testing description 1"},
    )
    response_data = response.json()
    created_id = response_data["id"]

    return int(created_id)


@pytest.fixture
async def created_workout_session_id(normal_user_client):
    response = await normal_user_client.post(
        "/workout-sessions", json={"comments": "testing post method 1"}
    )
    response_data = response.json()
    created_id = response_data["id"]
    return int(created_id)


@pytest.fixture
async def created_exercise_id(normal_user_client):
    response = await normal_user_client.post(
        f"/exercises",
        json={
            "name": "testing post method 1",
            "description": "testing description 1",
            "category": "testing category 1",
            "muscle_group": "testing muscle group 1",
        },
    )
    response_data = response.json()
    created_id = response_data["id"]

    return int(created_id)


@pytest.fixture
async def created_exericse_log_id(
    normal_user_client, created_workout_session_id, created_exercise_id
):
    response = await normal_user_client.post(
        f"/exercise-logs/workout-session/{created_workout_session_id}",
        json={
            "exercise_id": created_exercise_id,
            "sets": 1,
            "reps": 1,
            "intensity": 70,
            "exertion_scale": 9,
        },
    )

    response_data = response.json()
    created_id = response_data["id"]

    return int(created_id)
