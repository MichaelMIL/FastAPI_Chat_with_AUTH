from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from lib.dynamo_db.table import DynamoTable
from models.connection_model import Connection


connections_router = APIRouter()


@connections_router.post('/{FromUserPhone}/to/{ToUSerPhone}', response_model=Connection)
async def create_new_connection(
    request:Request, FromUserPhone:str, ToUserPhone:str
):
    if not ToUserPhone:
        return False
    users_table:DynamoTable = request.app.users_table
    from_user = users_table.query_items('phone', str(FromUserPhone), 'phone-index')
    to_user = users_table.query_items('phone', str(ToUserPhone), 'phone-index')
    if from_user and to_user:
        connections_table:DynamoTable = request.app.connections_table
        new_connection = Connection(from_user_id=from_user[0]['id'], to_user_id=to_user[0]['id'])
        connections_table.add_item(new_connection.dict())
        return new_connection
    else:
        raise HTTPException(404,'User not found')


@connections_router.put('activate/{ConnectionId}')
async def approve_pending_connection(
    request:Request,
    ConnectionId: str
):
    table: DynamoTable = request.app.connections_table
    table.update_item_by_dict({'id': ConnectionId},{'is_approved': True})