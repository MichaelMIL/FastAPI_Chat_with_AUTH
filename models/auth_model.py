from pydantic import BaseModel


class Token(BaseModel):
    id: str  # User ID
    phone: str  # User Phone
    exp: int  # im mins
