import pytest
from httpx import AsyncClient, ASGITransport
from project import app as fastapi_app
from fastapi import Request
from fastapi_azure_auth.user import User
from project import azure_scheme
from tortoise.contrib.test import finalizer, initializer
import asgi_lifespan


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "sqlite://:memory"  # Use in-memory SQLite for tests
    initializer(["models"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)

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
    response_1 = await normal_user_client.post("/workout-plans", json={"name": "testing post method 1", "description": "testing description 1"})
    assert response_1.status_code == 200
    response_data = response_1.json()
    created_id = response_data["id"]
    assert response_data["name"] == "testing post method 1"
    assert response_data["description"] is not None
    return int(created_id)

@pytest.mark.anyio
async def test_create_workout_plan(normal_user_client):
    response_1 = await normal_user_client.post("/workout-plans", json={"name": "testing post method 2", "description": "testing description 2"})
    response_2 = await normal_user_client.post("/workout-plans", json={"name": "testing lacking field"})
    print("secondly created", response_1)
    assert response_1.status_code == 200
    assert response_2.status_code == 422
    response_data = response_1.json()
    assert response_data["name"] == "testing post method 2"
    assert response_data["description"] is not None

@pytest.mark.anyio
async def test_get_workout_plans(normal_user_client):
    response = await normal_user_client.get("/workout-plans")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) != 0

@pytest.mark.anyio
async def test_get_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.get(f"/workout-plan/{created_workout_plan_id}")
    assert response_1.status_code == 200
    response_data_1 = response_1.json()
    assert response_data_1["id"] == created_workout_plan_id
    assert response_data_1["name"] == "testing post method 1"
    assert response_data_1["description"] == "testing description 1"

@pytest.mark.anyio
async def test_update_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.patch(f"/workout-plan/{created_workout_plan_id}", json={"name": "testing new workout plan", "description": "testing new description"})
    response_2 = await normal_user_client.get(f"/workout-plan/{created_workout_plan_id}")

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    response_data_1 = response_1.json()
    response_data_2 = response_2.json()

    assert response_data_1["name"] == response_data_2["name"]
    assert response_data_1["description"] == response_data_2["description"]

@pytest.mark.anyio
async def test_delete_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.delete(f"/workout-plan/{created_workout_plan_id}")
    response_2 = await normal_user_client.get(f"/workout-plan/{created_workout_plan_id}")
    response_3 = await normal_user_client.delete(f"/workout-plan/{123}")

    assert response_1.status_code == 204
    assert response_2.status_code == 500
    assert response_3.status_code == 500

