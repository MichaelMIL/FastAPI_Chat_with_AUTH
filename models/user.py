from pydantic import BaseModel, EmailStr
from typing import Optional



class User(BaseModel):
    Id: str = 'test-id'
    Name: str = 'test-name'
    Phone: str = '123456789'
    Email: EmailStr = 'user@test.com'
    Password: str= '1234'
    LookingFor: Optional[str] = 'Nada'
    Location: Optional[dict] = {'lat': 12.12, 'lon': 14.14}
    ProfilePicS3: Optional[str] = 'S3-Backet-path'