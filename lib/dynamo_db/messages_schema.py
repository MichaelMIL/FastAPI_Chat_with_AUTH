messages_schema = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'connection_id', 'KeyType': 'HASH'},
            {'AttributeName': 'creation_time', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'connection_id', 'AttributeType':'S'},
            {'AttributeName': 'creation_time', 'AttributeType':'S'},

        ]   
    },
    'secondery_keys': []
}