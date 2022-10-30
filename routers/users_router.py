from typing import List, Optional
from fastapi import APIRouter, Body, Request, Depends
from fastapi import APIRouter
from models.user import CreateUser, User, UpdateUser
from src.dynamo_db.table import DynamoTable

user_router = APIRouter()

def add_hints(var:DynamoTable):
    return var


@user_router.post('/{user_id}', response_model=User)
async def create_user(request: Request,user: CreateUser = Body(...)):
    request.app.users_table.add_item(user.dict())
    return user

@user_router.get('/{user_id}', response_model=User)
async def get_user(request: Request,user_id:str):
    user = request.app.users_table.query_items('id', user_id)
    return user[0]

@user_router.get('/phone/{user_phone}', response_model=User)
async def get_user_by_phone(request: Request,user_phone:str):
    user = request.app.users_table.query_items('phone', user_phone, 'phone-index')
    return user[0]

@user_router.delete('/{user_id}', response_model=None)
async def delete_user(request: Request,user_id:str):
    request.app.users_table.delete_item({'id': user_id})

@user_router.put('/{user_id}', response_model=dict)
async def update_user(request: Request,user_id:str, user = Body(...)):
    print(user)
    updated_user = request.app.users_table.update_item_by_dict(key={'id': user_id}, dict = user)
    # print(updated_user)
    return updated_user