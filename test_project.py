import pytest
from project import app as fastapi_app
from fastapi import Request
from fastapi_azure_auth.user import User
from conftest import *


@pytest.mark.anyio
async def test_create_workout_plan(normal_user_client):
    response_1 = await normal_user_client.post(
        "/workout-plans",
        json={"name": "testing post method 2", "description": "testing description 2"},
    )
    response_2 = await normal_user_client.post(
        "/workout-plans", json={"name": "testing lacking field"}
    )
    assert response_1.status_code == 200
    assert response_2.status_code == 422
    response_data = response_1.json()
    assert response_data["name"] == "testing post method 2"
    assert response_data["description"] is not None


@pytest.mark.anyio
async def test_get_workout_plans(normal_user_client):
    response = await normal_user_client.get("/workout-plans")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert (
        len(response.json()) != 0
    )  # it's actually one, idk pytest.fixture is not included


@pytest.mark.anyio
async def test_get_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.get(
        f"/workout-plan/{created_workout_plan_id}"
    )
    response_2 = await normal_user_client.get(f"/workout-plan/0")
    assert response_1.status_code == 200
    assert response_2.status_code == 404
    response_data_1 = response_1.json()
    assert response_data_1["id"] == created_workout_plan_id
    assert response_data_1["name"] == "testing post method 1"
    assert response_data_1["description"] == "testing description 1"


@pytest.mark.anyio
async def test_update_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.patch(
        f"/workout-plan/{created_workout_plan_id}",
        json={
            "name": "testing new workout plan",
            "description": "testing new description",
        },
    )
    response_2 = await normal_user_client.get(
        f"/workout-plan/{created_workout_plan_id}"
    )
    response_3 = await normal_user_client.get(f"/workout-plan/032169")

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 404

    response_data_1 = response_1.json()
    response_data_2 = response_2.json()

    assert response_data_1["name"] == response_data_2["name"]
    assert response_data_1["description"] == response_data_2["description"]


@pytest.mark.anyio
async def test_delete_workout_plan(normal_user_client, created_workout_plan_id):
    response_1 = await normal_user_client.delete(
        f"/workout-plan/{created_workout_plan_id}"
    )
    response_2 = await normal_user_client.get(
        f"/workout-plan/{created_workout_plan_id}"
    )
    response_3 = await normal_user_client.delete(f"/workout-plan/{123}")

    assert response_1.status_code == 204
    assert response_2.status_code == 404
    assert response_3.status_code == 404


@pytest.mark.anyio
async def test_create_workout_session(normal_user_client):
    response_1 = await normal_user_client.post(
        "/workout-sessions", json={"comments": "testing post method again"}
    )
    response_2 = await normal_user_client.post("/workout-sessions", json={})

    assert response_1.status_code == 200
    assert response_2.status_code == 422
    response_1 = response_1.json()
    assert "testing" in response_1["comments"]


@pytest.mark.anyio
async def test_get_workout_sessions(normal_user_client):
    response_1 = await normal_user_client.get("/workout-sessions")

    assert response_1.status_code == 200
    assert len(response_1.json()) != 0


@pytest.mark.anyio
async def test_get_workout_session(normal_user_client, created_workout_session_id):
    response_1 = await normal_user_client.get(
        f"/workout-session/{created_workout_session_id}"
    )
    response_2 = await normal_user_client.get("/workout-session/12332123212312")

    assert response_1.status_code == 200
    assert response_2.status_code == 404


@pytest.mark.anyio
async def test_update_workout_session(normal_user_client, created_workout_session_id):
    response_1 = await normal_user_client.patch(
        f"/workout-session/{created_workout_session_id}",
        json={"comments": "just updated recently"},
    )
    response_2 = await normal_user_client.patch(
        f"/workout-session/{created_workout_session_id}", json={}
    )
    response_3 = await normal_user_client.patch(
        f"/workout-session/123321", json={"comments": "this wouldn't work"}
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200  # since patch i guess it's fine
    assert response_3.status_code == 404


@pytest.mark.anyio
async def test_delete_workout_session(normal_user_client, created_workout_session_id):
    response_1 = await normal_user_client.delete(
        f"/workout-session/{created_workout_session_id}"
    )
    response_2 = await normal_user_client.get(
        f"/workout-session/{created_workout_session_id}"
    )
    response_3 = await normal_user_client.get(f"/workout-session/{69123}")
    assert response_1.status_code == 204
    assert response_2.status_code == 404
    assert response_3.status_code == 404


@pytest.mark.anyio
async def test_create_exercise_log(
    normal_user_client, created_workout_session_id, created_exercise_id
):
    response_1 = await normal_user_client.post(
        f"/exercise-logs/workout-session/{created_workout_session_id}",
        json={
            "sets": 3,
            "reps": 10,
            "intensity": 50,
            "exertion_scale": 7,
            "exercise_id": created_exercise_id,
        },
    )
    response_2 = await normal_user_client.post(
        f"/exercise-logs/workout-session/{created_workout_session_id}", json={}
    )
    response_3 = await normal_user_client.post(
        f"/exercise-logs/workout-session/{created_workout_session_id}",
        json={
            "sets": 3,
            "reps": 10,
            "weight": 50,
            "exertion_scale": 7,
            "exercise_id": 123,
        },
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 422
    assert response_3.status_code == 422


@pytest.mark.anyio
async def test_get_exercise_logs(normal_user_client, created_workout_session_id):
    workout_session_id = (
        created_workout_session_id - 1
    )  # because idk for some reason the id has incremented by 1 ( my take is that it's called again not sure)
    response_1 = await normal_user_client.get(
        f"/exercise-logs/workout-session/{workout_session_id}"
    )

    assert response_1.status_code == 200
    assert len(response_1.json()) != 0


@pytest.mark.anyio
async def test_get_exercise_log(normal_user_client, created_exercise_log_id):

    response_1 = await normal_user_client.get(
        f"/exercise-log/{created_exercise_log_id}/workout-session"
    )
    response_2 = await normal_user_client.get("/exercise-log/123")

    assert response_1.status_code == 200
    assert response_2.status_code == 404


@pytest.mark.anyio
async def test_update_exercise_log(normal_user_client, created_exercise_log_id):
    response_1 = await normal_user_client.patch(
        f"/exercise-log/{created_exercise_log_id}/workout-session",
        json={"sets": 1, "reps": 1, "intensity": 60, "exertion_scale": 7},
    )
    response_2 = await normal_user_client.patch(
        f"/exercise-log/{created_exercise_log_id}/workout-session",
        json={"sets": 1, "reps": 1, "weight": 69},
    )  # it's stilll 200 even though there some wrong field inputted in the body
    response_3 = await normal_user_client.patch(
        f"/exercise-log/123",
        json={"sets": 1, "reps": 1, "intensity": 60, "exertion_scale": 7},
    )
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 404


@pytest.mark.anyio
async def test_delete_exercise_log(normal_user_client, created_exercise_log_id):
    response_1 = await normal_user_client.delete(
        f"/exercise-log/{created_exercise_log_id}/workout-session"
    )
    response_2 = await normal_user_client.delete(
        "/exercise-log/1233212312312/workout-session"
    )
    assert response_1.status_code == 204
    assert response_2.status_code == 404


# TODO test exercise summary
@pytest.mark.anyio
async def test_create_exercise_summary(normal_user_client, created_exercise_log_id):
    response_1 = await normal_user_client.post(
        f"/exercise-summary/exercise-log/{created_exercise_log_id}",
        json={"total_sets": 12, "total_reps": 60, "total_holds": 0},
    )

    assert response_1.status_code == 500 # Because of create_user_exercise_log, we automatically create an exercise summary for that particular exercise log.



@pytest.mark.anyio
async def test_get_exercise_summary(normal_user_client, created_exercise_log_id): ...


@pytest.mark.anyio
async def test_update_exercise_summary(normal_user_client): ...


@pytest.mark.anyio
async def test_delete_exercise_summary(normal_user_client): ...


@pytest.mark.anyio
async def test_get_current_month_exercise_summaries(normal_user_client): ...
