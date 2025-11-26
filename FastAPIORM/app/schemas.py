from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserResp(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

class Book(BaseModel):
    id: Optional[int] = None
    bookName: str
    rating: Optional[float] = None
    isPublished: Optional[bool] = False
    publishedYear: Optional[int] = None
    created_at: Optional[datetime] = None
    owner_id: Optional[int] = None
    owner : Optional[UserResp] = None
    model_config = {
        "from_attributes": True
    }


class BookCreate(BaseModel):
    bookName: str
    rating: Optional[float] = None
    isPublished: Optional[bool] = False
    publishedYear: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]