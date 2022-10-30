users = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'id', 'KeyType': 'HASH'},
            {'AttributeName': 'phone', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'id', 'AttributeType':'S'},
            {'AttributeName': 'phone', 'AttributeType':'S'},

        ]   
    },
    'secondery_keys': [
        {
        'name' : 'phone-name-index',
        'key_schema' : [
            {'AttributeName': 'phone', 'KeyType': 'HASH'},
            {'AttributeName': 'id', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'id', 'AttributeType':'S'},
            {'AttributeName': 'phone', 'AttributeType':'S'},

        ]   
    }
    ]
}