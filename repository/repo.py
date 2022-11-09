


from models.database import user_table
from schema.schemas import ShowUser
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from models.database import user_table


def create_the_users(user: ShowUser):
    user = ShowUser(
        name=user.name,
        email=user.email,
        hashed_password = pwd_context.hash(user.password)
    )
    session.add(User)
    session.commit()
    session.close()
    return user


def get_user_by_email(email: str):

    session = Session(bind=engine, expire_on_commit=False)
    user = query(user_table).filter(user_table.email == email).first()
    session.close()
    return user