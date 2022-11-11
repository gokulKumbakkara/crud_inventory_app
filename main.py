from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import Base, engine, inventory, user_table
from schema import schemas
from security import oauth2, tokens

from routers import inventory, users

Base.metadata.create_all(engine)

tags_metadata = []

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(inventory.router)

# @app.get("/inventory/{id}",tags=["inventory"])
# def read_inventory_item(
#     id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
# ):

#     session = Session(bind=engine, expire_on_commit=False)

#     invent = session.query(inventory).get(id)

#     if not invent:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no items")

#     session.close()

#     return invent


# @app.post("/inventory", status_code=status.HTTP_201_CREATED,tags=["inventory"])
# def create_inventory(
#     request: schemas.InventoryRequest,
#     current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
# ):
#     session = Session(bind=engine, expire_on_commit=False)
#     inventory_instance = inventory(items=request.items, user_id=current_user.user_id)
#     session.add(inventory_instance)
#     session.commit()

#     id = inventory_instance.id
#     session.close()
#     return inventory_instance


# @app.put("/inventory/{id}",tags=["inventory"])
# def update_inventory(
#     id: int,
#     items: str,
#     current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
# ):

#     session = Session(bind=engine, expire_on_commit=False)

#     inventory_item = session.query(inventory).get(id)

#     if inventory_item:
#         inventory_item.items = items
#         session.commit()

#     session.close()

#     if not inventory_item:
#         raise HTTPException(
#             status_code=404,
#             detail=f"item with id {id} not found",
#         )

#     return inventory_item


# @app.delete("/inventory/{id}",tags=["inventory"])
# def delete_inventory_item(
#     id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
# ):

#     session = Session(bind=engine, expire_on_commit=False)
#     invent = session.query(inventory).get(id)

#     if invent:
#         session.delete(invent)
#         session.commit()
#         session.close()


# @app.get("/inventory",tags=["inventory"])
# def read_inventory(
#     current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
# ):

#     session = Session(bind=engine, expire_on_commit=False)

#     inventory_list = session.query(inventory).all()

#     session.close()

#     return inventory_list


@app.get("/user", tags=["user"])
def read_user(current_user: schemas.UserRequest = Depends(oauth2.get_current_user)):
    session = Session(bind=engine, expire_on_commit=False)

    user_data = session.query(user_table).all()

    session.close()

    return user_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=schemas.ShowUser, tags=["user"])
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


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["user"])
def read_user_id(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    session = Session(bind=engine, expire_on_commit=False)

    invent = session.query(user_table).get(id)

    session.close()

    return invent


@app.put("/user/{id}", tags=["user"])
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


@app.delete("/user/{id}", tags=["user"])
def delete_user(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
):

    session = Session(bind=engine, expire_on_commit=False)
    invent = session.query(user_table).get(id)

    if invent:
        session.delete(invent)
        session.commit()
        session.close()


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/login", tags=["login"])
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
