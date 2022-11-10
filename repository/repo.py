


from fastapi.security import OAuth2PasswordRequestForm
from models.database import engine, user_table
from passlib.context import CryptContext
from schema.schemas import ShowUser
from sqlalchemy.orm import Session


def create_the_users(user: ShowUser):
    user = ShowUser(
        name=user.name,
        email=user.email,
        hashed_password = pwd_context.hash(user.password)
    )
    session.add(user)
    session.commit()
    session.close()
    return user


def get_user_by_email(email: str):

    session = Session(bind=engine, expire_on_commit=False)
    user = session.query(user_table).filter(user_table.email == email).first()
    session.close()
    return user