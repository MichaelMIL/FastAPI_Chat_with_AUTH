from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from actions.auth_actions import verify_jwt_token
from lib.dynamo_db.table import DynamoTable
from models.connection_model import Connection
from actions.user_actions import _get_user_by_phone

connections_router = APIRouter()


@connections_router.post('/{FromUserPhone}/to/{ToUSerPhone}', response_model=Connection)
async def create_new_connection(
    request:Request, FromUserPhone:str, ToUserPhone:str,token : str =  Depends(verify_jwt_token)
):
    if not ToUserPhone or not FromUserPhone:
        raise HTTPException(404,'User not found')
    from_user = _get_user_by_phone(request,str(FromUserPhone))
    to_user = _get_user_by_phone(request,str(ToUserPhone))
    if from_user and to_user:
        connections_table:DynamoTable = request.app.connections_table
        new_connection = Connection(from_user_id=from_user['id'], to_user_id=to_user['id'])
        connections_table.add_item(new_connection.dict())
        return new_connection
    else:
        raise HTTPException(404,'User not found')


@connections_router.put('/activate/{ConnectionId}', response_model=dict)
async def approve_pending_connection(
    request:Request,
    ConnectionId: str,
    token : str =  Depends(verify_jwt_token)
):
    table: DynamoTable = request.app.connections_table
    table.update_item_by_dict({'id': ConnectionId},{'is_approved': True})
    return {'connection_id': ConnectionId,'is_approved': True}


@connections_router.get('/{UserPhone}/pending')
async def get_pending_connections(
    request: Request,
    UserPhone:str,
    token : str =  Depends(verify_jwt_token)
):
    user = _get_user_by_phone(request, UserPhone)
    table: DynamoTable = request.app.connections_table
    connections =  table.query_items('to_user_id',user['id'],'to_user_id-index')
    return [connection for connection in connections if connection['is_approved']==False]

@connections_router.get('/{UserPhone}/active')
async def get_active_connections(
    request: Request,
    UserPhone:str,
    token : str =  Depends(verify_jwt_token)
):
    user = _get_user_by_phone(request, UserPhone)
    table: DynamoTable = request.app.connections_table
    connections = [connection for connection in table.query_items('to_user_id',user['id'],'to_user_id-index') if connection['is_approved']==True] + [connection for connection in table.query_items('from_user_id',user['id'],'from_user_id-index') if connection['is_approved']==True]
    return connections


@connections_router.delete('/{ConnectionId}')
async def delete_connection(
    request:Request,
    ConnectionId: str,
    token : str =  Depends(verify_jwt_token)
):
    table: DynamoTable = request.app.connections_table
    table.delete_item({'id': ConnectionId})