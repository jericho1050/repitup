# Repitup

## Video Demo: TODO

### Description

**Repitup**: a backend workout logger app using Fastapi + Tortoise ORM with Azure B2C authentication

<!-- markdownlint-disable MD033 -->
<details>

<summary><h2>Walkthrough each module</h2></summary>

Let's walk through each python file and what it does.

### File Structure

```text
/repitup
├── Dockerfile
├── README.Docker.md
├── README.md
├── compose.yaml
├── conftest.py
├── controllers.py
├── database.py
├── env
├── helpers.py
├── migrations
├── models.py
├── project.py
├── pyproject.toml
├── requirements.txt
├── schemas.py
├── settings.py
└── test_project.py

directory: 2 file: 15

ignored: directory (1)
```

### `conftest.py`

In this configuration test file, the `@pytest.fixture`s' will be first executed, creating a user client and mockup data before running our test cases.

```py
# existing code..
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
# existing code..
```

### `controllers.py`

The `controllers.py` will define our helper functions that carry out the CRUD operations that are going to be called in `project.py`.

```py

async def get_user_workout_plans(user: User) -> list[WorkoutPlanBase]:
    """
    Retrieve workout plans for a user.

    :param user: The user for whom the workout plans are retrieved.
    :return: A list of workout plans in the response model format.
    :raises HTTPException: If there is an error retrieving the workout plans.
    :rtype: list[]
    """
    try:
        workout_plans = WorkoutPlan.filter(user=user)
        return await WorkoutPlan_Pydantic_List.from_queryset(workout_plans)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve workout plans: {e}"
        )
```

### `database.py`

The `database.py` contains our database connection code, responsible for communicating with the database, and our models module.

```py
# existing code..

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
# existing code..
```

### `helpers.py`

in this file it only contains few helper functions

```py
def get_db_uri(user, password, host, db):
    return f"postgres://{user}:{password}@{host}:5432/{db}"
```

### `models.py`

The `models.py` defines the database schema for **TORTOISE** to use. This allows **Tortoise ORM** to interact with the database using these models.

```py
# existing codes..

class WorkoutPlan(models.Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=25)
    description = fields.TextField()


class WorkoutSession(models.Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    date = fields.DatetimeField(auto_now_add=True)
    comments = fields.TextField()

# existing codes..
```

### `project.py`

In this file, we're now putting everything together in 'project.py' and defining our REST endpoints; it will now call our helper functions in `controllers.py` and act as an intermediary between the model and view in a MVC pattern.

```py
@app.get(
    "/workout-plan/{id}",
    response_model=WorkoutPlan_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def get_workout_plan(request: Request, id: int):
    """
    Retrieve a workout plan by its ID.

    Args:
        request (Request): The incoming request object.
        id (int): The ID of the workout plan to retrieve.

    Returns:
        WorkoutPlan_Pydantic: The retrieved workout plan.

    Raises:
        HTTPException: If the workout plan with the given ID does not exist.
    """
    user = await get_authenticated_user(request)
    return await get_user_workout_plan(id, user)


@app.post(
    "/workout-plans",
    response_model=WorkoutPlan_Pydantic,
    dependencies=[Security(azure_scheme)],
)
async def create_workout_plan(request: Request, workout_plan: WorkoutPlanCreate):
    """
    Create a new workout plan for the authenticated user.

    Args:
        request (Request): The incoming request object.
        workout_plan (WorkoutPlanCreate): The workout plan data to be created.

    Returns:
        WorkoutPlan_Pydantic: The created workout plan.

    Raises:
        HTTPException: If there is an error creating the workout plan.
    """
    user = await get_authenticated_user(request)
    return await create_user_workout_plan(user, workout_plan)
```

</details>

### Pre-resequite

- [FastApi-Azure B2C Authentication](https://intility.github.io/fastapi-azure-auth/b2c/azure_setup) (Azure Configuration)
- PostgreSQL Database Running (prefferably two, one for development and one for testing)

For authentication and the creation of user instances, you need to set FastApi-Azure B2C up, as it is necessary to interact with the Rest API.

## Installation

1. Clone this repository with

    ```zsh
    git clone https://github.com/me50/jericho1050.git
    ```

2. change directory to jericho1050 and then create a virtual enviroment

    ```zsh
    jericho1050 % virtualenv env
    ```

    or

    ```zsh
    jericho10050 % python -m env
    ```

3. Activate virtual enviroment

    windows users: `env\Scripts\activate.bat`

    MacOS users: `source env/bin/activate`

4. Install the dependencies in requirements.txt

    ```zsh
    (env) jericho1050 % pip install -r requirements.txt
    ```

5. Assuming you have configured and read the [FastApi-Azure B2C Authentication](https://intility.github.io/fastapi-azure-auth/b2c/azure_setup) documentation for ***Azure configuration section***, preferrably name your env file as `.env.azure` and `.env.database`.

    Your `.env.azure` should look like this

    ```shell
    TENANT_NAME="YOUR_TENANT_NAME"
    APP_CLIENT_ID="YOUR_CLIENT_ID_HERE"
    OPENAPI_CLIENT_ID="YOUR_CLIENT_ID_HERE"
    AUTH_POLICY_NAME="B2C_1_sign_up_sign_in"
    ```

    and your `.env.database` should look like this

    ```shell
    # POSTGRE CONFIG
    USERNAME="YOUR_USERNAME"
    PASSWORD="YOUR_PASSWORD"
    HOST="127.0.0.1"
    DB="YOUR_DATABASE" # your primary database
    TEST_DB="TEST_YOUR_DATABASE" # (optional) your testing database locally
    ```

    then your File Structure should be similar here

    ```text
    /jericho1050
    ├── Dockerfile
    ├── README.Docker.md
    ├── README.md
    ├── compose.yaml
    ├── conftest.py
    ├── controllers.py
    ├── database.py
    ├── env
    ├── .env.azure
    ├── .env.database
    ├── helpers.py
    ├── models.py
    ├── project.py
    ├── pyproject.toml
    ├── requirements.txt
    ├── schemas.py
    ├── settings.py
    └── test_project.py
    ```

6. In this step we will now be ~~migrating~~ initializing our models into our database

    **note**: if you don't have `pyproject.toml`

    then initalize first the config with `aerich init -t database.TORTOISE_ORM`

    ```shell
    jericho1050 % aerich init -t database.TORTOISE_ORM
    Success create migrate location ./migrations
    Success write config to pyproject.toml
    ```

    if there's, lets go initialize the db with

    ```shell
    jericho1050 % aerich init-db
    Success create app migrate location migrations/models
    Success generate schema for app "models"
    ```

    Cool, now you just generated your database schema. and there should be directory called `migrations`

7. in this final step you can now run the project

```shell
    jericho1050 % python project.py
    ...
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ...
```

For Comprehensive Rest API Documentation (OpenAPI) is at `http://127.0.0.1:8000/docs`

## Docker

Make sure you have Docker Desktop installed and that it is opened. Also,  deactivate your virtual environment.

1. Clone this Repo

    ```shell
    git clone https://github.com/me50/jericho1050.git
    ```

2. Assuming you have configured and read the [FastApi-Azure B2C Authentication](https://intility.github.io/fastapi-azure-auth/b2c/azure_setup) documentation for ***Azure configuration section***, preferrably name your env file as `.env.azure` and `.env.database`.

    your `.env.database` should look like this

    ```shell
    # DOCKER CONFIG
    USERNAME="test"
    PASSWORD="password"
    DB="yourdb"
    HOST="db"
    TEST_DB="TEST_YOUR_DATABASE" # optional
    ```

    and still Your `.env.azure` should look like this

    ```shell
    TENANT_NAME="YOUR_TENANT_NAME"
    APP_CLIENT_ID="YOUR_CLIENT_ID_HERE"
    OPENAPI_CLIENT_ID="YOUR_CLIENT_ID_HERE"
    AUTH_POLICY_NAME="B2C_1_sign_up_sign_in"
    ```

3. let's build our image then run our created container

```shell
jericho1050 % docker-compose build
jericho1050 % docker-compose up
```

that's it enjoy

## Testing

In this application, we're using the Pytest framework.
Just a reminder: make sure you have these in your env variables in your `.env.database` and your virtual enviroment (with the dependencies installed) is activated.

```shell
USERNAME="YOUR_USERNAME"
PASSWORD="YOUR_PASSWORD"
HOST="127.0.0.1"
TEST_DB="TEST_YOUR_DATABASE" # your running test postgre database locally
```

Okay let's go test the app by running in your terminal

```shell
jericho1050 % pytest test_project.py
```
