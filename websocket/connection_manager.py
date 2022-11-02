from dataclasses import dataclass
from typing import List

from fastapi import WebSocket


@dataclass
class UserWebSocket:
    user_id: str
    websocket: WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[UserWebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(
            UserWebSocket(user_id=user_id, websocket=websocket)
        )

    def disconnect(self, websocket: UserWebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_message_to_user(self, message: str, user_id: str):
        for connection in self.active_connections:
            if connection.user_id == user_id:
                await self.send_personal_message(
                    message=message, websocket=connection.websocket
                )

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.websocket.send_text(message)
