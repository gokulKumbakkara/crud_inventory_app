import json
from fastapi import Depends
import pytest
from main import app


def test_create_inventory(normal_user_token_headers):
    data = {"items": "gadgets"}
    response = normal_user_token_headers.post("/inventory", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["items"] == "gadgets"


def test_read_inventory(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.get("/inventory")
    assert response.status_code == 200


def test_update_inventory(normal_user_token_headers):
    
    session = normal_user_token_headers
    response = session.put("inventory/1",params={"items":"apple"})
    assert response.status_code == 200



def test_read_single_inventory(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.get("/inventory/4")
    assert response.status_code == 200
    assert response.json()["user_id"] == 2



def test_delete_inventory(normal_user_token_headers):
    session = normal_user_token_headers
    response = session.delete("inventory/2")
    assert response.status_code == 200
