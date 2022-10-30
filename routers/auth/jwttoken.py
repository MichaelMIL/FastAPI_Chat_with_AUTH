from datetime import datetime, timedelta
from jose import JWTError, jwt
from server.models.auth_model import TokenData

from server.config import secrets


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode, key=secrets.SECRET_KEY, algorithm=secrets.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(
            token=token, key=secrets.SECRET_KEY, algorithms=[secrets.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, exp=payload.get("exp"))
        return token_data
    except JWTError:
        raise credentials_exception
