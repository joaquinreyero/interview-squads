from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class SignInInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class SignInOutput(BaseModel):
    token: str
    id: int


class SignUpInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class SignUpOutput(BaseModel):
    token: str
    email: str


class User(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None


class TokenData(BaseModel):
    token: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None


class AuthenticateInput(BaseModel):
    token: str
