

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request, HTTPException, status, Depends, APIRouter
from lib.auth.OTP import rand_pass
from actions.auth_actions import authenticate_user, verify_jwt_token
from lib.auth.jwttoken import create_access_token
from lib.dynamo_db.table import DynamoTable




auth_router = APIRouter()

class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        
@auth_router.post("/token")
async def login_oauth(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    access_token = authenticate_user(data=form_data, request=request)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post('/otp', response_model=dict)
async def generate_otp(
    request: Request,
    token : str =  Depends(verify_jwt_token)
):
    table: DynamoTable = request.app.otps_table
    password = rand_pass(10)
    table.add_item({'key':password})
    return {'key':password}

@auth_router.post('/otp/{key}')
async def login_otp(
    request: Request,
    key:str
):
    if not key:
        raise InvalidCredentials
    table: DynamoTable = request.app.otps_table
    item = table.get_item({'key':key})
    if item:
        table.delete_item({'key':key})
        token = create_access_token({'key':key})
        return {"access_token": token, "token_type": "bearer"}
    raise InvalidCredentials

