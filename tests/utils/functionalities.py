
from fastapi.testclient import TestClient
from fastapi import Depends
from models.database import get_db
from schema import schemas
from sqlalchemy.orm import Session
import sys,os,string,random
from repository.repo import get_user_by_email,create_the_users
from models.database import engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 


from repository.repo import create_the_users,get_user_by_email

def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/login", data=data)
    response = r.json()
    print(f"[***response***]", response)
    assert r.status_code == 200
    auth_token = response["access_token"]
    print(auth_token)
    headers = {"Authorization": f"{response['token_type']} {response['access_token']}"}
    client.headers.update(headers)
    print(client.headers)
    return client


def authentication_token_from_email(client: TestClient, email: str,dbTest: Session):
    
    password = "string"
    name = "gokul"
    is_superuser = True
    user = get_user_by_email(email=email,dbTest=dbTest)
    if not user:
        
        user_in_create = schemas.UserRequest(name=name, email=email, password=password,is_superuser=is_superuser)
        user = create_the_users(user=user_in_create,dbTest=dbTest)
    return user_authentication_headers(client=client, email=email, password=password)

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))