
from fastapi import APIRouter, Body, Request, Depends
from fastapi import APIRouter
from actions.auth_actions import verify_jwt_token
from models.user_model import CreateUser, User
from lib.dynamo_db.table import DynamoTable

user_router = APIRouter()

@user_router.post('/{user_id}', response_model=User)
async def create_user(request: Request,user: CreateUser = Body(...),token : str =  Depends(verify_jwt_token)):
    table:DynamoTable = request.app.users_table
    table.add_item(user.dict())
    return user

@user_router.get('/{user_id}', response_model=User)
async def get_user(request: Request,user_id:str,token : str =  Depends(verify_jwt_token)):
    table:DynamoTable = request.app.users_table
    user = table.query_items('id', user_id)
    return user[0]

@user_router.get('/phone/{user_phone}', response_model=User)
async def get_user_by_phone(request: Request,user_phone:str,token : str =  Depends(verify_jwt_token)):
    table:DynamoTable = request.app.users_table
    user = table.query_items('phone', user_phone, 'phone-index')
    return user[0]

@user_router.delete('/{user_id}', response_model=None)
async def delete_user(request: Request,user_id:str,token : str =  Depends(verify_jwt_token)):
    table:DynamoTable = request.app.users_table
    table.delete_item({'id': user_id})

@user_router.put('/{user_id}', response_model=dict)
async def update_user(request: Request,user_id:str, user = Body(...),token : str =  Depends(verify_jwt_token)):
    table:DynamoTable = request.app.users_table
    updated_user = table.update_item_by_dict(key={'id': user_id}, dict = user)
    return updated_user