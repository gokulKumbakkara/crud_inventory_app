from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    email: Union[str, None] = None


class InventoryRequest(BaseModel):
    items: str


class ShowInventory(BaseModel):
    items: str
    name: str


class UserRequest(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True