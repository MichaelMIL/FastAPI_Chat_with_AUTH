from fastapi import Depends, HTTPException

from server.actions.sensor_actions import get_sensor
from .jwttoken import verify_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from server.models.user_model import User
from server.actions.exceptions.auth_exceptions import InvalidCredentials
from server.actions.exceptions.user_exceptions import UserNotAdmin
from server.enums.user_enums import UserRole
from server.actions.user_actions import get_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = InvalidCredentials
    return verify_token(token, credentials_exception)


def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = InvalidCredentials
    return verify_token(token, credentials_exception)


async def get_current_active_user(
    request: Request, current_user: User = Depends(get_current_user)
) -> User:
    current_user = current_user.dict()
    if current_user["exp"] <= 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        user = get_user(filter={"username": str(current_user["username"])}, request=request)
        return user


def get_user_by_token(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> User:
    token = verify_jwt_token(token)
    user = get_user(filter={"username": token.username}, request=request)
    return user


async def is_current_user_admin(
    current_user: User = Depends(get_current_active_user),
) -> bool:
    if current_user.role == UserRole.ADMIN:
        return True
    else:
        raise UserNotAdmin


def sensor_api_key_auth(request: Request, api_key: str) -> bool:
    sensor = get_sensor(filter={"key": api_key}, request=request)
    if sensor is None:
        raise InvalidCredentials
    return sensor
