from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
import pytest
from tests.utils.functionalities import authentication_token_from_email,random_char
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from models.database import Base,get_db

generated_email=random_char(8)+"@gmail.com"

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, dbTest: Session):
    client = TestClient(app)

    return authentication_token_from_email(client=client, email=generated_email,dbTest=dbTest)


@pytest.fixture(scope="module")
def naive_session():
    return TestClient(app)
