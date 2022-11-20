from fastapi import APIRouter
from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.database import get_db

from models.database import Base, engine, inventory, user_table
from schema import schemas
from security import oauth2, tokens



router = APIRouter()


@router.get("/user",tags=["user"])
def read_user(db: Session = Depends(get_db),current_user: schemas.UserRequest = Depends(oauth2.get_current_user)):

    user_data = db.query(user_table).all()


    return user_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user", response_model=schemas.DisplayUser,tags=["user"])
def create_user(
    request: schemas.UserRequest,db: Session = Depends(get_db),current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    hashed_password = pwd_context.hash(request.password)
    if current_user.is_superuser == True:
        user_instance = user_table(
            name=request.name, email=request.email, password=hashed_password,is_superuser=request.is_superuser
        )
        db.add(user_instance)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"no privilege"
        )

    return user_instance


@router.get("/user/{id}", response_model=schemas.ShowUser,tags=["user"])
def read_user_id(
    id: int,db: Session = Depends(get_db),current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):


    invent = db.query(user_table).get(id)

    db.close()
    print("#######")
    print(invent.id)
  
    print("######")

    return invent


@router.put("/user/{id}",tags=["user"])
def update_inventory(
    id: int,
    name: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):


    user_data = db.query(user_table).get(id)

    if user_data:
        user_data.name = name
        db.commit()

    if not user_data:
        raise HTTPException(status_code=404, detail=f"item with id {id} not found")
    print(user_data)
    return user_data


@router.delete("/user/{id}",tags=["user"])
def delete_user(
    id: int,db: Session = Depends(get_db), current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    invent = db.query(user_table).get(id)

    if invent:
        db.delete(invent)
        db.commit()
    