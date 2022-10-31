from pydantic import BaseModel, Field
from typing import Optional
import secrets
from time import time

class Connection(BaseModel):
    id: str = Field(default_factory= lambda: secrets.token_hex(16))
    from_user_id: str
    to_user_id: str
    is_approved: bool = False
    creation_time: int = Field(default_factory= lambda: int(time()))