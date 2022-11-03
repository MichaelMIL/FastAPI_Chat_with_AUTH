users_schema = {
    "base": {
        "key_schema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "attribute_definitions": [{"AttributeName": "id", "AttributeType": "S"}],
    },
    "secondary_keys": [
        {
            "name": "phone-index",
            "key_schema": [
                {"AttributeName": "phone", "KeyType": "HASH"},
            ],
            "attribute_definitions": [
                {"AttributeName": "phone", "AttributeType": "S"},
            ],
        },
        {
            "name": "phone-password-index",
            "key_schema": [
                {"AttributeName": "phone", "KeyType": "HASH"},
                {"AttributeName": "password", "KeyType": "RANGE"},
            ],
            "attribute_definitions": [
                {"AttributeName": "phone", "AttributeType": "S"},
                {"AttributeName": "password", "AttributeType": "S"},
            ],
        },
    ],
}
