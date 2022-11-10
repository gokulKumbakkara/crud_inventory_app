from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    email: Union[str, None] = None
    user_id: Union[str, None] = None


class InventoryRequest(BaseModel):
    items: str


class ShowInventory(BaseModel):
    id: int


class UserRequest(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class CurrentUser(BaseModel):
    id: int
    email: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
