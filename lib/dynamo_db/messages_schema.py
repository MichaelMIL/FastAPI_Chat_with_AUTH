messages_schema = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'connection_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'connection_id', 'AttributeType':'S'},
            {'AttributeName': 'timestamp', 'AttributeType':'S'},

        ]   
    },
    'secondery_keys': []
}