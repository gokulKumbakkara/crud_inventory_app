from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    email: Union[str, None] = None
    user_id: Union[str, None] = None
    is_superuser:Union[str,None] = None


class InventoryRequest(BaseModel):
    items: Union[str, None] = None


class ShowInventory(BaseModel):
    id: Union[int, None] = None


class UserRequest(BaseModel):
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    is_superuser: bool




class Token(BaseModel):
    access_token: Union[str, None] = None
    token_type: Union[str, None] = None

class CurrentUser(BaseModel):
    user_id: Union[int, None] = None
    email: Union[str, None] = None
    is_superuser: bool


class ShowUser(BaseModel):
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    is_superuser: bool

class DisplayUser(BaseModel):
    name: Union[str, None] = None
    email: Union[str, None] = None
    is_superuser: bool

    class Config:
        orm_mode = True
