from typing import Union
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from actions.auth_actions import verify_jwt_token
from lib.dynamo_db.table import DynamoTable
from models.auth_model import Token
from models.message_model import Message
from websocket.connection_manager import ConnectionManager, UserWebSocket
import json

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


@websocket_router.websocket("/{ConnectionId}")
async def websocket_endpoint(
    websocket: WebSocket,
    ConnectionId: str,
    token: Token = Depends(get_token),
):
    connections_table: DynamoTable = (
        websocket.app.connections_table
    )  # Get the connections table
    messages_table: DynamoTable = websocket.app.messages_table  # get messages table
    connection = connections_table.get_item(
        {"id": ConnectionId}
    )  # Find the required connection
    if not connection:
        return None  # if no connection was found - dont establish WS connection

    # Determine if the user is 'from' or 'to' user
    if connection["from_user_id"] == token["id"]:
        # print(f"connected as from_user")
        dest = connection["to_user_id"]
    elif connection["to_user_id"] == token["id"]:
        # print(f"connected as to_user")
        dest = connection["from_user_id"]

    await manager.connect(websocket, token["id"])  # Waiting for WS connection
    try:
        await manager.send_message_to_user(
            f"{token['phone']} joined the chat", dest
        )  # Announce that user has been joined the chat

        # Get last 30 messages
        old_messages = messages_table.query_items(
            "connection_id", connection["id"], asc=False, limit=30
        )
        old_messages.reverse()

        # Send each one to the newly connected user
        for msg in old_messages:
            await manager.send_personal_message(
                json.dumps(Message(**msg).dict()), websocket
            )

        while True:
            data = await websocket.receive_text()  # waiting for user message

            # Creating a Message
            msg = Message(
                connection_id=connection["id"],
                content=data,
                from_user_id=token["id"],
            )
            await manager.send_personal_message(
                json.dumps(msg.dict()), websocket
            )  # Sending the message object (as JSON string) back to the user
            await manager.send_message_to_user(
                json.dumps(msg.dict()), dest
            )  # Sending the message object (as JSON string) to other user
            messages_table.add_item(msg.dict())  # Logging the message to DB
    except WebSocketDisconnect:
        manager.disconnect(
            UserWebSocket(websocket=websocket, user_id=token["id"])
        )  # Disconnect
        await manager.send_message_to_user(
            f"{token['phone']} left the chat", dest
        )  # Announce that user has left
