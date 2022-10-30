# from typing import Union, List

# from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status, WebSocketDisconnect
# from fastapi.responses import HTMLResponse

# app = FastAPI()



# import AWS boto3
import boto3
# import DynamoDB table class
from src.dynamo_db.table import DynamoTable

# import needed schemas
from src.dynamo_db.connections_schema import connections
from src.dynamo_db.users_schema import users
from src.dynamo_db.messages_schema import messages

# creeating a clinet for connectiong DynamoDb
resource = boto3.resource('dynamodb')

# load/create needed tables
# users_table = DynamoTable('users', resource, users['key_schema'], users['attribute_definitions'])
# connections_table = DynamoTable('connections', resource, connections['key_schema'], connections['attribute_definitions'])
# messages_table = DynamoTable('messages', resource, messages['key_schema'], messages['attribute_definitions'])


test_table = DynamoTable('test', resource, users)
print(test_table.attributes)
print(test_table.query_items('id','123'))

