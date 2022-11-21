from typing import Optional, Union

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.database import Base, engine, get_db, inventory, user_table
from passlib.context import CryptContext
from pydantic import BaseModel
from schema import schemas
from security import oauth2, tokens
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/user",tags=["user"])
def read_user(db: Session = Depends(get_db))->user_table:
    user_data = db.query(user_table).all()


    return user_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user", response_model=schemas.DisplayUser,tags=["user"])
def create_user(
    request: schemas.UserRequest,db: Session = Depends(get_db),current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
)->user_table:

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


@router.get("/user/{id}",tags=["user"])
def read_user_id(
    id: int,db: Session = Depends(get_db),current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
)->user_table:


    invent =db.query(user_table).filter(user_table.id == id).first()

    db.close()

    return invent


@router.put("/user/{id}",tags=["user"])
def update_user(
    id: int,
    name: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
)->user_table:


    user_data = db.query(user_table).get(id)

    if user_data:
        user_data.name = name
        db.commit()

    if not user_data:
        raise HTTPException(status_code=404, detail=f"item with id {id} not found")
    return user_data


@router.delete("/user/{id}",tags=["user"])
def delete_user(
    id: int,db: Session = Depends(get_db), current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
)->Union[str,None]:

    invent = db.query(user_table).get(id)

    if invent:
        db.delete(invent)
        db.commit()
    