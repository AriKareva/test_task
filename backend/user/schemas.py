from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str
    email: str
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    ...


class UserUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    user_id: int
    

class UserSignIn(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True


class AccessTokenResponse(BaseModel):
    user_id: int  
    login: str  
    access_token: str
    token_type: str = 'bearer'


class AccessTokenPayload(BaseModel):
    user_id: int
    login: str
