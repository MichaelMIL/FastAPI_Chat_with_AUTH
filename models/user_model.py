from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import secrets

from configs import PHONE_LEN


class User(BaseModel):
    id: str = Field(default_factory=lambda: secrets.token_hex(16))  # Unique ID
    user_name: str
    phone: str = Field(..., max_length=PHONE_LEN)
    email: EmailStr
    school: str
    looking_for: Optional[str]
    user_location: Optional[dict]


class CreateUser(User):
    user_name: str
    phone: str = Field(..., max_length=PHONE_LEN)
    email: EmailStr
    password: str
    school: str
    looking_for: Optional[str]
    user_location: Optional[dict]


class UpdateUser(BaseModel):
    user_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    school: Optional[str]
    looking_for: Optional[str]
    user_location: Optional[dict]
    password: Optional[str]
