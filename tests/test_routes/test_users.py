import json
import pytest
from fastapi import Depends
from main import app


def test_create_user(normal_user_token_headers):
    data = {
        "name": "gokul",
        "email": "JMOyghac@gmail.com",
        "password": "string",
        "is_superuser": False
    }
    print(normal_user_token_headers.headers["authorization"])
    response = normal_user_token_headers.post("/user", json=data)

    print(response.text)
    assert response.status_code == 200
    assert response.json()["email"] == "JMOyghac@gmail.com"


def test_read_user(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.get("/user")
    
    assert response.status_code == 200

def test_update_user(normal_user_token_headers):
    # data = {
    #     "id": "1",
    #     "name": "google",
    # }
    #/user/2" 

    params = {
        "name":"google"
    }
    session = normal_user_token_headers
    response = session.put("/user/1", params=params)
    assert response.status_code == 200
 

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
