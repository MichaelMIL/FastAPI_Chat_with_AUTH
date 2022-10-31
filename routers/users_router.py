
from fastapi import APIRouter, Body, Request, Depends
from fastapi import APIRouter
from actions.auth_actions import verify_jwt_token
from models.user_model import CreateUser, User
from actions.user_actions import _create_user,_delete_user,_get_user,_get_user_by_phone,_update_user

user_router = APIRouter()

@user_router.post('/', response_model=User)
async def create_user(request: Request,user: CreateUser = Body(...),token : str =  Depends(verify_jwt_token)):
    user = _create_user(request=request,user=user)
    return user

@user_router.get('/{UserId}', response_model=User)
async def get_user(request: Request,UserId:str,token : str =  Depends(verify_jwt_token)):
    user = _get_user(request=request,user_id=UserId)
    return user

@user_router.get('/phone/{UserPhoneNumber}', response_model=User)
async def get_user_by_phone(request: Request,UserPhoneNumber:str,token : str =  Depends(verify_jwt_token)):
    user = _get_user_by_phone(request=request, user_phone=UserPhoneNumber)
    return user

@user_router.delete('/{UserId}', response_model=None)
async def delete_user(request: Request,UserId:str,token : str =  Depends(verify_jwt_token)):
    _delete_user(request=request, user_id=UserId)

@user_router.put('/{UserId}', response_model=dict)
async def update_user(request: Request,UserId:str, user:dict = Body(...),token : str =  Depends(verify_jwt_token)):
    updated_user = _update_user(request=request, user_id=UserId, user=user)
    return updated_user