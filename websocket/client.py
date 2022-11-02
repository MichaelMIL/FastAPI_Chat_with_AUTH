from typing import Union
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from pydantic import Field
from actions.auth_actions import verify_jwt_token
from models.auth_model import Token
from websocket.connection_manager import ConnectionManager, UserWebSocket


websocket_router = APIRouter()
manager = ConnectionManager()


async def get_token(
    websocket: WebSocket,
    token: Union[str, None] = Query(default=None),
) -> Token:
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        token_data = verify_jwt_token(token=token)
    return token_data


@websocket_router.websocket("/{ConnectioId}")
async def websocket_endpoint(
    websocket: WebSocket,
    ConnectioId: str,
    token: Token = Depends(get_token),
):
    connection = websocket.app.connections_table.get_item({"id": ConnectioId})
    if not connection:
        return None
    if connection["from_user_id"] == token["id"]:
        # print(f"connected as from_user")
        dest = connection["to_user_id"]
    elif connection["to_user_id"] == token["id"]:
        # print(f"connected as to_user")
        dest = connection["from_user_id"]
    await manager.connect(websocket, token["id"])
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.send_message_to_user(data, dest)
            # await manager.broadcast(f"Client #{ConnectioId} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(UserWebSocket(websocket=websocket, user_id=token["id"]))
        # await manager.broadcast(f"Client #{ConnectioId} left the chat")
        await manager.send_message_to_user(f"{token['phone']} left the chat", dest)
