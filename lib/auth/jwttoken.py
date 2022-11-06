from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "09d232643253a2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> dict:
    try:
        payload = jwt.decode(token=str(token), key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        phone = payload.get("phone")
        if phone is None and id is None:
            return {"exp": payload.get("exp")}
        token_data = {"id": id, "phone": phone, "exp": payload.get("exp")}
        return token_data
    except JWTError:
        raise credentials_exception
