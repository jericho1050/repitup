import os
from helpers import get_db_uri
from dotenv import load_dotenv

load_dotenv(".env.database")

# Tortoise ORM configuration
TORTOISE_ORM = {
    "connections": {
        "default": get_db_uri(
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            db=os.getenv("DB"),
        ),
    },
    "apps": { 
        "models": {
            "models": ["aerich.models", "models"],  # Specify the location of your models
            "default_connection": "default",
        },
    },
}
