from fastapi.testclient import TestClient
import pytest


# def test_status(client: TestClient):
#     response = client.get("/ping")
#     assert response.status_code == 200
#     assert response.json() == {"ping": "pong"}


@pytest.fixture
def create_app_user(client: TestClient):
    data = {"username": "mike", "password": "123"}
    res = client.post("/api/v1/app-users", json=data)
    assert res.status_code == 201
    yield res.json()


# def test_create_app_user(create_app_user):
#     user = create_app_user

#     assert user["username"] == "mike"
#     assert user["password"] == "123"

#     assert "id" in user
#     assert "created_at" in user


# def test_get_app_user(client: TestClient, create_app_user):
#     user = create_app_user
#     id = user["id"]
#     res = client.get(f"/api/v1/app-users/{id}")

#     assert res.status_code == 200
#     assert res.json()["id"] == user["id"]
#     assert res.json()["username"] == user["username"]
#     assert res.json()["password"] == user["password"]
#     assert res.json()["created_at"] == user["created_at"]

#     id = user["id"] + 1
#     res = client.get(f"/api/v1/app-users/{id}")
#     assert res.status_code == 404
#     assert res.json() == {"detail": "Not Found"}


# def test_update_app_user(client: TestClient, create_app_user):
#     user= create_app_user
#     id = user["id"]
#     res = client.patch(f"/api/v1/app-users/{id}", json={"password": "456"})

#     assert res.status_code == 200
#     assert res.json()["id"] == user["id"]
#     assert res.json()["username"] == user["username"]
#     assert res.json()["password"] == "456"
#     assert res.json()["created_at"] == user["created_at"]


def test_delete_app_user(client: TestClient, create_app_user):
    user = create_app_user
    id = user["id"]

    res = client.delete(f"/api/v1/app-users/{id}")
    assert res.status_code == 200
    assert res.json() is None

    res = client.get(f"/api/v1/app-users/{id}")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
