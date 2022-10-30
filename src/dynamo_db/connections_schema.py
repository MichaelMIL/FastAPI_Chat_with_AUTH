connections = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        'attribute_definitions' : [
            {'AttributeName': 'id', 'AttributeType':'S'},
        ]   
    },
    'secondery_keys': [
        {
        'name' : 'from_user_id-to_user_id-index',
        'key_schema' : [
            {'AttributeName': 'from_user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'is_approved', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'from_user_id', 'AttributeType':'S'},
            {'AttributeName': 'is_approved', 'AttributeType':'B'},

        ]   
    },
    {
        'name' : 'to_user_id-from_user_id-index',
        'key_schema' : [
            {'AttributeName': 'to_user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'is_approved', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'to_user_id', 'AttributeType':'S'},
            {'AttributeName': 'is_approved', 'AttributeType':'B'},

        ]   
    },
    ]
}