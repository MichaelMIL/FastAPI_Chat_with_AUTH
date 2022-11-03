connections_schema = {
    "base": {
        "key_schema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "attribute_definitions": [
            {"AttributeName": "id", "AttributeType": "S"},
        ],
    },
    "secondary_keys": [
        {
            "name": "from_user_id-index",
            "key_schema": [
                {"AttributeName": "from_user_id", "KeyType": "HASH"},
            ],
            "attribute_definitions": [
                {"AttributeName": "from_user_id", "AttributeType": "S"},
            ],
        },
        {
            "name": "to_user_id-index",
            "key_schema": [
                {"AttributeName": "to_user_id", "KeyType": "HASH"},
            ],
            "attribute_definitions": [
                {"AttributeName": "to_user_id", "AttributeType": "S"},
            ],
        },
    ],
}
