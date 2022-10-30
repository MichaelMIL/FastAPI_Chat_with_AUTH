users = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        'attribute_definitions' : [
            {'AttributeName': 'id', 'AttributeType':'S'}
        ]   
    },
    'secondery_keys': [
        {
        'name' : 'phone-index',
        'key_schema' : [
            {'AttributeName': 'phone', 'KeyType': 'HASH'},
        ],
        'attribute_definitions' : [
            {'AttributeName': 'phone', 'AttributeType':'S'},
        ]   
    }
    ]
}