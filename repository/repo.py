


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from models.database import engine, user_table
from passlib.context import CryptContext
from schema.schemas import ShowUser
from sqlalchemy.orm import Session
from models.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_the_users(user: ShowUser,dbTest: Session):
    user = ShowUser(
        name=user.name,
        email=user.email,
        hashed_password = pwd_context.hash(user.password)
    )
    dbTest.add(user)
    dbTest.commit()
    dbTest.close()
    return user


def get_user_by_email(email: str,dbTest: Session):

    user = dbTest.query(user_table).filter(user_table.email == email).first()
    return user

def verify(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)