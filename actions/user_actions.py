
from lib.dynamo_db.table import DynamoTable
from fastapi import HTTPException, Request
from models.user_model import CreateUser, User

def _create_user(request: Request,user: CreateUser)->User:
    table:DynamoTable = request.app.users_table
    table.add_item(user.dict())
    return User(**user)


def _get_user(request: Request,user_id:str)->User:
    table:DynamoTable = request.app.users_table
    user = table.query_items('id', user_id)
    if not len(user) >0:
        raise HTTPException(404, f'User not found ({user_id})')
    return User(**user[0])


def _get_user_by_phone(request: Request,user_phone:str)->User:
    table:DynamoTable = request.app.users_table
    user = table.query_items('phone', str(user_phone), 'phone-index')
    if not len(user) >0:
        raise HTTPException(404, f'User not found ({user_phone})')
    return User(**user[0])


def _delete_user(request: Request,user_id:str)->None:
    table:DynamoTable = request.app.users_table
    table.delete_item({'id': user_id})


def _update_user(request: Request,user_id:str, user:dict)->dict:
    table:DynamoTable = request.app.users_table
    updated_user = table.update_item_by_dict(key={'id': user_id}, dict = user)
    if not updated_user:
        raise HTTPException(400, 'Missing body')
    return updated_user