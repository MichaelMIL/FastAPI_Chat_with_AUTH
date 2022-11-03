from pydantic import BaseModel, Field
import secrets
from time import time


class Connection(BaseModel):
    id: str = Field(default_factory=lambda: secrets.token_hex(16))  # Unique ID
    from_user_id: str  # User ID of the user who created the connection
    to_user_id: str  # User ID of the user which the connection created for
    is_approved: bool = False  # If 'to_user_id' approve - will set to True
    creation_time: int = Field(default_factory=lambda: int(time()))  # in seconds
