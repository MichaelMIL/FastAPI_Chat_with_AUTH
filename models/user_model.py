from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import secrets


class User(BaseModel):
    id: str = Field(default_factory=lambda: secrets.token_hex(16))
    user_name: str
    phone: str = Field(..., max_length=10)
    email: EmailStr
    school: str
    looking_for: Optional[str]
    user_location: Optional[dict]
    profile_pic_S3_path: Optional[str]


class CreateUser(User):
    user_name: str
    phone: str = Field(..., max_length=10)
    email: EmailStr
    password: str
    school: str
    looking_for: Optional[str]
    user_location: Optional[dict]
    profile_pic_S3_path: Optional[str]


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
