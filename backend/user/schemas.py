from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str
    email: str

class UserCreate(UserBase):
    ...

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    ...
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    ...
    
    class Config:
        from_attributes = True