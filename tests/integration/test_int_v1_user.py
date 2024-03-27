from fastapi.testclient import TestClient


def test_status(client: TestClient):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_create_user(client: TestClient):
    data = {"username": "mike", "password": "789"}
    res = client.post("/api/v1/users", json=data)

    assert res.status_code == 201
    assert res.json()["id"] == 3
    assert res.json()["username"] == "mike"
    assert res.json()["password"] == "789"
    assert "id" in res.json()
    assert "created_at" in res.json()


def test_get_user(client: TestClient):
    res = client.get("/api/v1/users/1")

    assert res.status_code == 200
    assert res.json()["id"] == 1
    assert res.json()["username"] == "nick"
    assert res.json()["password"] == "123"
    assert "created_at" in res.json()

    res = client.get("/api/v1/users/3")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}


def test_update_user(client: TestClient):
    res = client.patch("/api/v1/users/2", json={"password": "000"})

    assert res.status_code == 200
    assert res.json()["id"] == 2
    assert res.json()["username"] == "alex"
    assert res.json()["password"] == "000"
    assert "created_at" in res.json()


def test_delete_app_user(client: TestClient):
    res = client.delete("/api/v1/users/2")
    assert res.status_code == 200
    assert res.json() is None

    res = client.get("/api/v1/users/2")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
