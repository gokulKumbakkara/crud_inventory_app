import httpx
import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from main import app
from models.database import Base, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from tests.utils.functionalities import (authentication_token_from_email,
                                         random_char)

dbTest=SessionLocal()

generated_email=random_char(8)+"@gmail.com"

@pytest.fixture(scope="module")
def normal_user_token_headers():
    client = TestClient(app)

    return authentication_token_from_email(client=client, email=generated_email,dbTest=dbTest)


@pytest.fixture(scope="module")
def naive_session():
    return TestClient(app)
