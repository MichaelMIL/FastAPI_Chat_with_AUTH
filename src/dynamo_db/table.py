from typing import List
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import boto3

class DynamoTable:
    def __init__(self,table_name ,dyn_resource, table_schema:dict=None) -> None:
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table_name = table_name
        self.table = None
        self._sec_indexs = []
        if not self.exists():
            if table_schema:
                print(f'Table {table_name} is missing - creating table')
                self.create_table_and_sec_indexs(table_schema)
            else:
                print(f'Table {table_name} is missing - create table')

    @property
    def attributes(self)->List:
        return self.table.attribute_definitions

    @property
    def sec_indexs(self) ->List:
        return self._sec_indexs

    def create_table_and_sec_indexs(self, table_schema:dict):
        self.create(key_schema = table_schema['base']['key_schema'],attribute_definitions=table_schema['base']['attribute_definitions'])
        for sec_index in table_schema['secondery_keys']:
            self.add_sec_index(index_name= sec_index['name'], key_schema= sec_index['key_schema'],attribute_definitions=sec_index['attribute_definitions'])


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
                "Couldn't add item %s to table %s. Here's why: %s: %s",
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
                "Couldn't get item %s from table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']

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

    def query_items(self, key_name:str, equals:str, sec_index_name:str = None):
        """
        Queries for items.
        :return: The list of items.
        """
        try:
            if sec_index_name:
                response = self.table.query(IndexName=sec_index_name,
                KeyConditionExpression=Key(key_name).eq(equals))
            else:    
                response = self.table.query(KeyConditionExpression=Key(key_name).eq(equals))
        except ClientError as err:
            print("Couldn't query for items. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Items']


    def scan_items(self, range):
        """
        Scans for items that.
        Uses a projection expression to return a subset of data for each item.
        :return: The list of items released in the specified years.
        """
        items = []
        scan_kwargs = {'FilterExpression': Key('year').between(range['first'], range['second'])}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs['ExclusiveStartKey'] = start_key
                response = self.table.scan(**scan_kwargs)
                items.extend(response.get('Items', []))
                start_key = response.get('LastEvaluatedKey', None)
                done = start_key is None
        except ClientError as err:
            print(
                "Couldn't scan for items. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

        return items


    def update_item(self,key:dict ,update_expression:str="set info.rating=:r, info.plot=:p", update_values:str='":r": {VALUE}, ":p": {VALUE}'):
        """
        Updates data for an item in the table.
        :return: The fields that were updated, with their new values.
        """
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
            client = boto3.client('dynamodb')
            resp = client.update_table(
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
                                "ReadCapacityUnits": 10,
                                "WriteCapacityUnits": 10,
                            }
                        }
                    }
                ],
            )
            print("Secondary index added!")
            self._sec_indexs.append(index_name)
        except Exception as e:
            print("Error updating table:")
            print(e)

    