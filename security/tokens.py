import os
from datetime import datetime, timedelta
from typing import Union

from dotenv import load_dotenv
import jwt
from schema import schemas

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        is_superuser: str = payload.get("is_superuser")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, user_id=user_id,is_superuser=is_superuser)
        return token_data
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
