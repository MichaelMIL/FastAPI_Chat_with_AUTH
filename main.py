from fastapi import FastAPI

# main FastAPI app
app = FastAPI()

# import AWS boto3
import boto3

# import DynamoDB table class
from lib.dynamo_db.table import DynamoTable

# import needed schemas
from lib.dynamo_db.connections_schema import connections_schema
from lib.dynamo_db.users_schema import users_schema
from lib.dynamo_db.messages_schema import messages_schema
from lib.dynamo_db.OTP_schema import otp_schema

# creeating a clinet for connectiong DynamoDb
resource = boto3.resource("dynamodb")
client = boto3.client("dynamodb")

# import routers
from routers.users_router import user_router
from routers.auth_router import auth_router
from routers.connections_router import connections_router
from websocket.client import websocket_router


@app.on_event("startup")
def startup_db_client():
    # load/create needed tables
    app.users_table = DynamoTable("users", resource, client, users_schema)
    app.connections_table = DynamoTable(
        "connections", resource, client, connections_schema
    )
    app.messages_table = DynamoTable("messages", resource, client, messages_schema)
    app.otps_table = DynamoTable("otps", resource, client, otp_schema)


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(connections_router, prefix="/connections", tags=["connections"])
app.include_router(websocket_router, prefix="/message", tags=["message"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000,
    )
