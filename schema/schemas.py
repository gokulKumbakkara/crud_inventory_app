from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    email: Union[str, None] = None
    user_id: Union[str, None] = None
    is_superuser:Union[str,None] = None


class InventoryRequest(BaseModel):
    items: str


class ShowInventory(BaseModel):
    id: int


class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    is_superuser: bool




class Token(BaseModel):
    access_token: str
    token_type: str

class CurrentUser(BaseModel):
    user_id: int
    email: str
    is_superuser: bool


class ShowUser(BaseModel):
    name: str
    email: str
    password: str

class DisplayUser(BaseModel):
    name: str
    email: str
    is_superuser: bool

    class Config:
        orm_mode = True
