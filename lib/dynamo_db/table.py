from typing import List, Union
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import time


def expression_and_values_builder(dict:dict, command:str) ->Union[str,dict]:
    expression = command
    values = {}
    for key, value in dict.items():
        expression += f' {key}=:{key},'
        values[f':{key}'] = value
    return expression[:-1] , values

class DynamoTable:
    def __init__(self,table_name:str ,dyn_resource, dyn_client, table_schema:dict=None) -> None:
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.dyn_client = dyn_client
        self.table_name = table_name
        self.table = None
        self._sec_indexes = []
        if not self.exists():
            if table_schema:
                print(f'Table {table_name.upper()} is missing - creating table')
                self.create_table_and_sec_indexes(table_schema)
            else:
                print(f'Table {table_name.upper()} is missing - create table')

    @property
    def attributes(self)->List:
        return self.table.attribute_definitions

    @property
    def sec_indexes(self) ->List:
        return self._sec_indexes

    @property
    def describe_table(self)->dict:
        return self.dyn_client.describe_table(TableName=self.table_name)

    @property
    def global_secondary_indexes(self)-> List[dict]:
        return self.describe_table['Table']['GlobalSecondaryIndexes']

    @property
    def global_secondary_indexes_list(self)-> List[str]:
        return [name['IndexName'] for name in self.describe_table['Table']['GlobalSecondaryIndexes']]

    def create_table_and_sec_indexes(self, table_schema:dict):
        self.create(key_schema = table_schema['base']['key_schema'],attribute_definitions=table_schema['base']['attribute_definitions'])
        time.sleep(1)
        for sec_index in table_schema['secondary_keys']:
            self.add_sec_index(index_name= sec_index['name'], key_schema= sec_index['key_schema'],attribute_definitions=sec_index['attribute_definitions'])
            time.sleep(1)



    def exists(self):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.
        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(self.table_name)
            table.load()
            exists = True
            self.table = table
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                print(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    self.table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        return exists



    def create(self, key_schema:List[dict] = [{'AttributeName': 'id', 'KeyType': 'HASH'},{'AttributeName': 'name', 'KeyType': 'RANGE'}], attribute_definitions:List[dict]=[{'AttributeName': 'id', 'AttributeType': 'S'}, {'AttributeName': 'name', 'AttributeType': 'S'}]):
        """
        Creates an Amazon DynamoDB table that can be used to store data.
        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=self.table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
            print(f'Waiting for {self.table_name} to be created')
            self.table.wait_until_exists()
        except ClientError as err:
            print(
                "Couldn't create table %s. Here's why: %s: %s", self.table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.table


    def list_all_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.
        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            print(
                "Couldn't list tables. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return tables

    def delete_table(self):
        """
        Deletes the table.
        """
        try:
            self.table.delete()
            self.table = None
        except ClientError as err:
            print(
                "Couldn't delete table. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise


    def add_item(self, item:dict):
        """
        Adds an item to the table.
        """
        try:
            self.table.put_item(Item=item)
        except ClientError as err:
            print(
                "Couldn't add item %s to table %s. Here's why: %s: %s",item,
                 self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def get_item(self, key:dict):
        """
        Gets item from the table for a specific key.
        :return: The data about the requested item.
        """
        try:
            response = self.table.get_item(Key=key)
        except ClientError as err:
            print(
                "Couldn't get item %s from table %s. Here's why: %s: %s", key,
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            if 'Item' in response:
                return response['Item']
            return None

    def delete_item(self, key):
        """
        Deletes a item from the table.
        """
        try:
            self.table.delete_item(Key=key)
        except ClientError as err:
            print(
                "Couldn't delete item %s. Here's why: %s: %s",err.response['Error']['Code'], err.response['Error']['Message'])
            raise


    def query_items(self, key_name:str, equals, sec_index_name:str = None, sec_key:str = None, sec_equals=None, asc=True, limit=100):
        """
        Queries for items.
        :return: The list of items.
        """
        try:
            if sec_index_name:
                if sec_key and sec_equals:
                    response = self.table.query(IndexName=sec_index_name,
                    KeyConditionExpression=Key(key_name).eq(equals) & Key(sec_key).eq(sec_equals),ScanIndexForward=asc,Limit=limit
                    )
                else:
                    response = self.table.query(IndexName=sec_index_name,
                    KeyConditionExpression=Key(key_name).eq(equals),ScanIndexForward=asc,Limit=limit)
            else:   
                if sec_key and sec_equals:
                    response = self.table.query(KeyConditionExpression=Key(key_name).eq(equals) & Key(sec_key).eq(sec_equals),ScanIndexForward=asc,Limit=limit) 
                else:
                    response = self.table.query(KeyConditionExpression=Key(key_name).eq(equals),ScanIndexForward=asc,Limit=limit)
        except ClientError as err:
            print("Couldn't query for items. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            if 'Items' in response:
                return response['Items']
            return []

    def get_all_items(self):
        items = self.table.scan()
        if "Items" in items:
            return items['Items']
        else:
            return None

    def update_item_by_dict(self,key:dict, dict:dict):
        update_expression,update_values = expression_and_values_builder(dict, 'set')
        return self.update_item(key,update_expression,update_values)

    def update_item(self,key:dict ,update_expression:str="set info.rating=:r, info.plot=:p", update_values:dict='":r": {VALUE}, ":p": {VALUE}'):
        """
        Updates data for an item in the table.
        :return: The fields that were updated, with their new values.
        """
        if not update_expression or not update_values:
            return None
        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=update_values,
                ReturnValues="UPDATED_NEW")
        except ClientError as err:
            print(
                "Couldn't update item in table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Attributes']

    def add_sec_index(self,index_name:str, key_schema:List[dict],attribute_definitions:List[dict], projection_type:str="ALL"):
        try:
            resp = self.dyn_client.update_table(
                TableName=self.table_name,
                # Any attributes used in your new global secondary index must be declared in AttributeDefinitions
                AttributeDefinitions=attribute_definitions,
                # This is where you add, update, or delete any global secondary indexes on your table.
                GlobalSecondaryIndexUpdates=[
                    {
                        "Create": {
                            # You need to name your index and specifically refer to it when using it for queries.
                            "IndexName": index_name,
                            # Like the table itself, you need to specify the key schema for an index.
                            # For a global secondary index, you can use a simple or composite key schema.
                            "KeySchema": key_schema,
                            # You can choose to copy only specific attributes from the original item into the index.
                            # You might want to copy only a few attributes to save space.
                            "Projection": {
                                "ProjectionType": projection_type
                            },
                            # Global secondary indexes have read and write capacity separate from the underlying table.
                            "ProvisionedThroughput": {
                                "ReadCapacityUnits": 2,
                                "WriteCapacityUnits": 2,
                            }
                        }
                    }
                ],
            )
            created = False
            print('Waiting for secondary index to be created and active (between few seconds to few mins)')
            while not created:
                indexes = self.global_secondary_indexes
                for index in indexes:
                    if index['IndexName'] == index_name and index['IndexStatus'] == 'ACTIVE':
                        print("Secondary index added!")
                        print(f'Index {index_name} was created')
                        self._sec_indexes.append(index_name)
                        created = True
                print(f'Waiting for secondary index ({index_name}) to be created ....')
                time.sleep(10)
            
        except Exception as e:
            print("Error updating table:")
            print(e)

    