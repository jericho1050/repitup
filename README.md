# Repitup

## Video Demo: TODO

### Description

**Repitup**: a backend workout logger app using Fastapi + Tortoise ORM with Azure B2C authentication

### Pre-resequite

- [FastApi-Azure B2C Authentication](https://intility.github.io/fastapi-azure-auth/b2c/azure_setup)
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

5. 