connections = {
    'key_schema' : [
        {'AttributeName': 'type', 'KeyType': 'HASH'},
        {'AttributeName': 'id', 'KeyType': 'RANGE'},
        {'AttributeName': 'from_user', 'KeyType': 'RANGE'},
        {'AttributeName': 'to_user', 'KeyType': 'RANGE'},
        {'AttributeName': 'is_approved', 'KeyType': 'RANGE'},
    ],
    'attribute_definitions' : [
        {'AttributeName': 'type', 'AttributeType':'S'},
        {'AttributeName': 'id', 'AttributeType':'S'},
        {'AttributeName': 'from_user', 'AttributeType':'S'},
        {'AttributeName': 'to_user', 'AttributeType':'S'},
        {'AttributeName': 'is_approved', 'AttributeType':'BOOL'},
    ]
}

messages = {
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