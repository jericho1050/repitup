import pytest, os, bcrypt
from dotenv import load_dotenv
from helpers import get_db_uri
from tortoise.contrib.test import finalizer, initializer
from tortoise.exceptions import DoesNotExist
from schemas import *
from models import *

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "sqlite://:memory"  # Use in-memory SQLite for tests
    initializer(["models"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)

@pytest.mark.asyncio
async def test_create_user():
    user_dict = {"username": "testuser", "password": "secret", "email": "testuser@gmail.com"}
    user_instance = await User.create(**user_dict)
    await user_instance.save()

    try:
        retrieved_instance = await User.get(id=user_instance.id)
        assert retrieved_instance.username == "testuser"
        assert bcrypt.hashpw("secret".encode(), bcrypt.gensalt()).decode() == retrieved_instance.password

        assert retrieved_instance.email == "testuser@gmail.com"
    except DoesNotExist:
        pytest.fail("User not found in the database.")

