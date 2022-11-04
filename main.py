from fastapi import FastAPI


# main FastAPI app
app = FastAPI()

# import AWS boto3
import boto3

# import DynamoDB table class
from lib.dynamo_db.table import DynamoTable

# import S3 bucket class
from lib.s3.bucket import S3_Bucket

# import configs
from configs import HOST, PORT, S3_REGION, S3_BUCKET_NAME, OTP_DEFAULT

# import needed schemas
from lib.dynamo_db.connections_schema import connections_schema
from lib.dynamo_db.users_schema import users_schema
from lib.dynamo_db.messages_schema import messages_schema
from lib.dynamo_db.OTP_schema import otp_schema

# creating a client for connecting DynamoDb
resource = boto3.resource("dynamodb")
client = boto3.client("dynamodb")

# creating S3 resource
s3_resource = boto3.resource("s3", region_name=S3_REGION)
s3_client = boto3.client("s3", region_name=S3_REGION)


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
    # Adds One Time Password if no user exists
    users = app.users_table.get_all_items()
    if len(users) == 0:
        app.otps_table.add_item({"key": OTP_DEFAULT})
        print(f"New One Time Password was added ('{OTP_DEFAULT}')")


@app.on_event("startup")
def start_s3():
    app.s3_bucket = S3_Bucket(s3_resource, s3_client, S3_BUCKET_NAME, S3_REGION)


# Adding routes
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(connections_router, prefix="/connections", tags=["connections"])
app.include_router(websocket_router, prefix="/message", tags=["message"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=HOST,
        reload=True,
        port=PORT,
    )
