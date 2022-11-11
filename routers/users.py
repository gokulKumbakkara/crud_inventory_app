from fastapi import APIRouter
from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import Base, engine, inventory, user_table
from schema import schemas
from security import oauth2, tokens



router = APIRouter()


@router.get("/user",tags=["user"])
def read_user(current_user: schemas.UserRequest = Depends(oauth2.get_current_user)):
    session = Session(bind=engine, expire_on_commit=False)

    user_data = session.query(user_table).all()

    session.close()

    return user_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user", response_model=schemas.ShowUser,tags=["user"])
def create_user(
    request: schemas.UserRequest,
):

    session = Session(bind=engine, expire_on_commit=False)
    hashed_password = pwd_context.hash(request.password)
    user_instance = user_table(
        name=request.name, email=request.email, password=hashed_password
    )
    session.add(user_instance)
    session.commit()

    id = user_instance.id
    session.close()
    return user_instance


@router.get("/user/{id}", response_model=schemas.ShowUser,tags=["user"])
def read_user_id(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    session = Session(bind=engine, expire_on_commit=False)

    invent = session.query(user_table).get(id)

    session.close()

    return invent


@router.put("/user/{id}",tags=["user"])
def update_inventory(
    id: int,
    name: str,
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):

    session = Session(bind=engine, expire_on_commit=False)

    user_data = session.query(user_table).get(id)

    if user_data:
        user_data.name = name
        session.commit()

    session.close()

    if not user_data:
        raise HTTPException(status_code=404, detail=f"item with id {id} not found")

    return user_data


@router.delete("/user/{id}",tags=["user"])
def delete_user(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    session = Session(bind=engine, expire_on_commit=False)
    invent = session.query(user_table).get(id)

    if invent:
        session.delete(invent)
        session.commit()
        session.close()
    