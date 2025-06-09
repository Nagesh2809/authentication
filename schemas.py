from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: str
    mobile_number: str
    password: str
    is_admin: Optional[bool] = False  
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date

class ShowUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    mobile_number: str
    is_admin: bool
    jwt: str

    class Config:
        # orm_mode = True
          from_attributes = True

class ShowUserWithToken(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    mobile_number: str
    is_admin: bool
    jwt: str

    class Config:
        from_attributes = True

# # class Config:
#     from_attributes = True
