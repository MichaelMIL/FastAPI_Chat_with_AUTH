from pydantic import BaseModel, Field
import secrets
from time import time


class Message(BaseModel):
    connection_id: str  # Unique ID
    from_user_id: str  # User ID of the user who sent the message
    content: str  # Content of the message
    timestamp: int = Field(
        default_factory=lambda: int(time() * 1000)
    )  # in milliseconds
