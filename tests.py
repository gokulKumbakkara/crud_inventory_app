from fastapi.testclient import TestClient
from main import app
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from main import app

client = TestClient(app)

import json

def test_app():
    client = TestClient(app)
    response = client.get('/user')
    assert response.status_code == 200