otp_schema = {
    'base' : {
        'key_schema' : [
            {'AttributeName': 'key', 'KeyType': 'HASH'},
        ],
        'attribute_definitions' : [
            {'AttributeName': 'key', 'AttributeType':'S'},
        ]   
    },
    'secondery_keys': []
}
