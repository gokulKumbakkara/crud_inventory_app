from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status,Request
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import Base, engine, inventory, user_table
from schema import schemas
from security import oauth2, tokens

from routers import inventory, users,login

Base.metadata.create_all(engine)

tags_metadata = []

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(inventory.router)
app.include_router(users.router)
app.include_router(login.router)
