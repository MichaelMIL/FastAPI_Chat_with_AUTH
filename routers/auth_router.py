

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request, HTTPException, status, Depends, APIRouter
from actions.auth_actions import authenticate_user



auth_router = APIRouter()

class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        
@auth_router.post("/token")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    access_token = authenticate_user(data=form_data, request=request)
    return {"access_token": access_token, "token_type": "bearer"}


