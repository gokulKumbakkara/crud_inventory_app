from pydantic import BaseModel
from typing import Union

class TokenData(BaseModel):
    email: Union[str, None] = None

class inventoryRequest(BaseModel):
    items: str
    
class showInventory(BaseModel):
    items: str
    name: str

class userRequest(BaseModel):
    name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class showUser(BaseModel):
    name: str
    email: str
    
    class Config():
        orm_mode = True
