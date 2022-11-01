from pydantic import BaseModel

class Token(BaseModel):
    id:str
    phone:str
    exp:int