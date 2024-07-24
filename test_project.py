import pytest
from httpx import AsyncClient
from project import app as fastapi_app
from fastapi import Request
from fastapi_azure_auth.user import User
from project import azure_scheme
import asgi_lifespan

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
        async with AsyncClient(app=manager.app, base_url="http://test") as ac:
            yield ac

@pytest.mark.anyio
async def test_get_workout_plans(normal_user_client):
        response = await normal_user_client.get("/workout-plans")
        assert response.status_code == 200
        assert type(response.json()) == list

@pytest.fixture
def anyio_backend():
    return "asyncio"


