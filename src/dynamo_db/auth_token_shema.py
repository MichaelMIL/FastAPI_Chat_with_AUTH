
auth_token_schema = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'token', 'KeyType': 'HASH'},
            {'AttributeName': 'phone', 'KeyType': 'RANGE'},

        ],
        'attribute_definitions' : [
            {'AttributeName': 'token', 'AttributeType':'S'},
            {'AttributeName': 'phone', 'AttributeType':'S'},

        ]   
    },
    'secondery_keys': []
}