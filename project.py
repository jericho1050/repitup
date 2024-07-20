import os
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from helpers import get_db_uri
from dotenv import load_dotenv
import models

load_dotenv()

app = FastAPI()

# Corrected Tortoise ORM configuration
TORTOISE_ORM = {
    "connections": {
        "default": get_db_uri(
            user="jericho",
            password="test",
            host="127.0.0.1",
            db="mydatabase2",
        ),
    },
    "apps": {  # Corrected key here
        "models": {
            "models": ["models"],  # Specify the location of your models
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/db_check")
async def db_check():
    try:
        await models.User.first()
        return {"status": "Connected to the database successfully"}
    except Exception as e:
        # It's a good practice to log the exception message to understand the specific failure
        print(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")