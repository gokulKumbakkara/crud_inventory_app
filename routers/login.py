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
from repository.repo import verify



router = APIRouter()

@router.post("/login",tags=["login"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    session = Session(bind=engine, expire_on_commit=False)
    user = (
        session.query(user_table).filter(user_table.email == form_data.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials"
        )
    if not verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"incorrect password"
        )

    access_token = tokens.create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}