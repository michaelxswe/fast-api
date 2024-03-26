from fastapi.testclient import TestClient


def test_status(client: TestClient):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_create_user(client: TestClient):
    data = {"username": "mike", "password": "123"}
    res = client.post("/api/v1/users", json=data)

    assert res.status_code == 201
    assert res.json()["username"] == "mike"
    assert res.json()["password"] == "123"
    assert "id" in res.json()
    assert "created_at" in res.json()


def test_get_user(client: TestClient):
    data = {"username": "nick", "password": "123"}
    res = client.post("/api/v1/users", json=data)
    assert res.status_code == 201
    user = res.json()
    user_id = user["id"]

    res = client.get(f"/api/v1/users/{user_id}")

    assert res.status_code == 200
    assert res.json()["id"] == user["id"]
    assert res.json()["username"] == user["username"]
    assert res.json()["password"] == user["password"]
    assert res.json()["created_at"] == user["created_at"]

    id = user["id"] + 1
    res = client.get(f"/api/v1/users/{id}")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}


def test_update_user(client: TestClient):
    data = {"username": "alex", "password": "123"}
    res = client.post("/api/v1/users", json=data)
    assert res.status_code == 201
    user = res.json()
    user_id = user["id"]

    res = client.patch(f"/api/v1/users/{user_id}", json={"password": "456"})

    assert res.status_code == 200
    assert res.json()["id"] == user["id"]
    assert res.json()["username"] == user["username"]
    assert res.json()["password"] == "456"
    assert res.json()["created_at"] == user["created_at"]


def test_delete_app_user(client: TestClient):
    data = {"username": "eric", "password": "123"}
    res = client.post("/api/v1/users", json=data)
    assert res.status_code == 201
    user = res.json()
    user_id = user["id"]

    res = client.delete(f"/api/v1/users/{user_id}")
    assert res.status_code == 200
    assert res.json() is None

    res = client.get(f"/api/v1/users/{user_id}")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
