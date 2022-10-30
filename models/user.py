from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import secrets


class User(BaseModel):
    id: str = Field(default_factory= lambda: secrets.token_hex(16))
    user_name: str = 'test-name'
    phone: str = '123456789'
    email: EmailStr = 'user@test.com'
    looking_for: Optional[str] = 'Nada'
    user_location: Optional[dict] = {'lat': "12.12", 'lon': "14.14"}
    profile_pic_S3_path: Optional[str] = 'S3-Backet-path'

class CreateUser(User):
    user_name: str = 'test-name'
    phone: str = '123456789'
    email: EmailStr = 'user@test.com'
    password:str = '1234'
    looking_for: Optional[str] = 'Nada'
    user_location: Optional[dict] = {'lat': "12.12", 'lon': "14.14"}
    profile_pic_S3_path: Optional[str] = 'S3-Backet-path'


class UpdateUser(BaseModel):
    user_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    password:Optional[str]
    looking_for: Optional[str]
    user_location: Optional[dict]
    profile_pic_S3_path: Optional[str]

if __name__ == '__main__':
    user = CreateUser(name='test_name', phone='1111111', password='1111',email='user@test.com', looking_for='you',location={'lat':"123", 'lon':"3333"})
    print(user)