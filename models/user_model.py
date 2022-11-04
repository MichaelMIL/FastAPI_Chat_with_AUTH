from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import secrets

from configs import PHONE_LEN


class User(BaseModel):
    id: str = Field(default_factory=lambda: secrets.token_hex(16))
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


if __name__ == "__main__":
    user = CreateUser(
        name="test_name",
        phone="1111111",
        password="1111",
        email="user@test.com",
        looking_for="you",
        location={"lat": "123", "lon": "3333"},
    )
    print(user)
