import json
import pytest
from main import app


def test_create_user(naive_session):
    data = {
        "name": "gokul",
        "email": "gokull@g.com",
        "password": "string",
    }
    response = naive_session.post("/user", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "gokull@g.com"


def test_read_user(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.get("/user")
    
    assert response.status_code == 200

def test_update_user(normal_user_token_headers):
    data = {
        "id": "1",
        "name": "google",
    }
    session = normal_user_token_headers
    response = session.put("/user/2?name=google", data=data)
    assert response.status_code == 200
    assert response.json()["name"] == "google"
    assert response.json()["email"] == "gokull@g.com"
    assert response.json()["password"] == "$2b$12$xtUdCCUw5fApCrTggZ39Qem/LSyyiltdLG1z4TkpiCO7Ttf0YC5E."
    assert response.json()["id"] == 2

def test_read_single_user(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.get("/user/2")
    assert response.status_code == 200
    assert response.json()["name"] == "google"
    assert response.json()["email"] == "gokull@g.com"


def test_delete_user(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.delete("user/1")
    assert response.status_code == 200
