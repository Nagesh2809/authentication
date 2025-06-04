from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: str
    mobile_number: str
    password: str

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

    class Config:
        orm_mode = True
