from typing import Optional, Union

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.database import Base, engine, get_db, inventory, user_table
from passlib.context import CryptContext
from pydantic import BaseModel
from repository.repo import verify
from schema import schemas
from security import oauth2, tokens
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/login",tags=["login"])
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = (
        db.query(user_table).filter(user_table.email == form_data.username).first()
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
        data={"sub": user.email, "user_id": user.id,"is_superuser":user.is_superuser}
    )
    print("##################")
    print(access_token)
    print("##################")
    return {"access_token": access_token, "token_type": "bearer"}