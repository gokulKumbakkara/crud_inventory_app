from typing import Optional, Union

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.database import Base, engine, inventory, user_table
from passlib.context import CryptContext
from pydantic import BaseModel
from schema import schemas
from security import oauth2, tokens
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/inventory",tags=["inventory"])
def read_inventory(
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
) ->inventory: 

    session = Session(bind=engine, expire_on_commit=False)

    inventory_list = session.query(inventory).all()

    session.close()

    return inventory_list

@router.get("/inventory/{id}",tags=["inventory"])
def read_inventory_item(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
) ->inventory:

    session = Session(bind=engine, expire_on_commit=False)

    invent = session.query(inventory).get(id)

    if not invent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no items")

    session.close()

    return invent


@router.post("/inventory", status_code=status.HTTP_201_CREATED,tags=["inventory"])
def create_inventory(
    request: schemas.InventoryRequest,
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user),
)->inventory:
    session = Session(bind=engine, expire_on_commit=False)
    inventory_instance = inventory(items=request.items, user_id=current_user.user_id)
    session.add(inventory_instance)
    session.commit()

    id = inventory_instance.id
    session.close()
    return inventory_instance


@router.put("/inventory/{id}",tags=["inventory"])
def update_inventory(
    id: int,
    items: str,
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
)-> inventory:

    session = Session(bind=engine, expire_on_commit=False)

    inventory_item = session.query(inventory).get(id)

    if inventory_item:
        inventory_item.items = items
        session.commit()

    session.close()

    if not inventory_item:
        raise HTTPException(
            status_code=404,
            detail=f"item with id {id} not found",
        )

    return inventory_item


@router.delete("/inventory/{id}",tags=["inventory"])
def delete_inventory_item(
    id: int, current_user: schemas.UserRequest = Depends(oauth2.get_current_user)
) -> Union[str,None]:

    session = Session(bind=engine, expire_on_commit=False)
    invent = session.query(inventory).get(id)

    if invent:
        session.delete(invent)
        session.commit()
        session.close()