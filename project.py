from database import TORTOISE_ORM
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from models import *

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/db_check")
async def db_check():
    try:
        await User.first()
        return {"status": f"Connected to the database successfully"}
    except Exception as e:
        # It's a good practice to log the exception message to understand the specific failure
        print(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")