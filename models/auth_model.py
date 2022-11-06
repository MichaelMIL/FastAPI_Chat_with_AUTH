from pydantic import BaseModel


class Token(BaseModel):
    id: str  # User ID
    phone: str  # User Phone
    exp: int  # im mins


class BearerToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OTP(BaseModel):
    key:str
