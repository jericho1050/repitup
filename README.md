# Repitup

## Video Demo: TODO

### Description

**Repitup**: a backend workout logger app using Fastapi + Tortoise ORM with Azure B2C authentication

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
