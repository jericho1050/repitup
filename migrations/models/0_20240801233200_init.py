from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "object_id" VARCHAR(100) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "exercise" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "description" TEXT NOT NULL,
    "category" VARCHAR(50) NOT NULL,
    "muscle_group" VARCHAR(50) NOT NULL,
    "user_id" VARCHAR(100) NOT NULL REFERENCES "user" ("object_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "workoutplan" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(25) NOT NULL,
    "description" TEXT NOT NULL,
    "user_id" VARCHAR(100) NOT NULL REFERENCES "user" ("object_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "workoutsession" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "comments" TEXT NOT NULL,
    "user_id" VARCHAR(100) NOT NULL REFERENCES "user" ("object_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "calendarentry" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "workout_session_id" INT NOT NULL REFERENCES "workoutsession" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "exerciselog" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "sets" INT NOT NULL,
    "reps" INT NOT NULL,
    "intensity" INT NOT NULL,
    "exertion_scale" INT NOT NULL,
    "exercise_id" INT NOT NULL REFERENCES "exercise" ("id") ON DELETE CASCADE,
    "workout_session_id" INT NOT NULL REFERENCES "workoutsession" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "exercisesummary" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "total_sets" INT NOT NULL,
    "total_reps" INT NOT NULL,
    "total_holds" INT NOT NULL,
    "exercise_id" INT NOT NULL REFERENCES "exerciselog" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
