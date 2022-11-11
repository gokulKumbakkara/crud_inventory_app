from fastapi.testclient import TestClient
import pytest
from tests.utils.functionalities import authentication_token_from_email
from main import app


@pytest.fixture(scope="module")
def normal_user_token_headers():
    client = TestClient(app)

    return authentication_token_from_email(client=client, email="gokull@g.com")


@pytest.fixture(scope="module")
def naive_session():
    return TestClient(app)
