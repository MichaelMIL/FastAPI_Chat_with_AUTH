from pydantic import BaseModel, Field
import secrets
from time import time

class Message(BaseModel):
    id: str = Field(default_factory= lambda: secrets.token_hex(16))
    chat_id: str
    from_user_id: str
    content: str
    creation_time: int = Field(default_factory= lambda: int(time()))