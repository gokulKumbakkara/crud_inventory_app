import json
import pytest
from main import app


def test_login(naive_session):
    data = {
        "username": "gokull@g.com",
        "password": "string",
    }
    response = naive_session.post("/login", data=data)
    assert response.status_code == 200
