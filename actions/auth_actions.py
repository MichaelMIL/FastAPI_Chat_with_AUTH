from datetime import timedelta
from typing import List
from lib.auth.jwttoken import create_access_token, verify_token
from lib.dynamo_db.table import DynamoTable
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Request, HTTPException, status, Depends

from models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
ACCESS_TOKEN_EXPIRE_MINUTES = 10000


class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = InvalidCredentials
    return verify_token(token, credentials_exception)


def verify_password(phone: str, password: str, request: Request):
    table: DynamoTable = request.app.users_table
    res = table.query_items(
        "phone", phone, "phone-password-index", "password", password
    )
    if not len(res) > 0:
        return [False, None]
    return [True, User(**res[0])]


def authenticate_user(data: OAuth2PasswordRequestForm, request: Request) -> bool:
    phone = str(data.username)
    password = data.password
    is_verified, user_data = verify_password(phone, password, request)
    print(user_data)
    if is_verified:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.id, "phone": user_data.phone},
            expires_delta=access_token_expires,
        )
        return access_token
    else:
        raise InvalidCredentials
