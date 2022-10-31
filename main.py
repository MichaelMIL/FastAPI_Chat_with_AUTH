from typing import Union, List

from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse
# main FastAPI app
app = FastAPI()

# import AWS boto3
import boto3

# import DynamoDB table class
from lib.dynamo_db.table import DynamoTable

# import needed schemas
from lib.dynamo_db.connections_schema import connections
from lib.dynamo_db.users_schema import users
from lib.dynamo_db.messages_schema import messages
from lib.dynamo_db.OTP_schema import otp
from lib.dynamo_db.auth_token_shema import auth_token_schema

# creeating a clinet for connectiong DynamoDb
resource = boto3.resource("dynamodb")
client = boto3.client("dynamodb")

# import routers
from routers.users_router import user_router
from routers.auth_router import auth_router

@app.on_event("startup")
def startup_db_client():
    # load/create needed tables
    app.users_table = DynamoTable("users", resource, client, users)
    app.connections_table = DynamoTable("connections", resource, client, connections)
    app.messages_table = DynamoTable("messages", resource, client, messages)
    app.otps_table = DynamoTable('otps', resource,client, otp)
    
# app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000,
    )