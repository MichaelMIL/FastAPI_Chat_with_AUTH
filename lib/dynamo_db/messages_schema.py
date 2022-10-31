messages_schema = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'connection_id', 'KeyType': 'HASH'},
            {'AttributeName': 'id', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'connection_id', 'AttributeType':'S'},
            {'AttributeName': 'id', 'AttributeType':'S'},

        ]   
    },
    'secondery_keys': []
}