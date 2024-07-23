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
