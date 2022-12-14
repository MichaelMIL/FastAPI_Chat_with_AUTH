# Test env vars:
HOST = "0.0.0.0"
PORT = 8000

# First One Time Password
OTP_DEFAULT = "NewServer4267"

# S3
S3_REGION = "eu-central-1"  # Region
S3_BUCKET_NAME = "chat-profile-pictures"  # S3 bucket`s name

# Max phone number length
PHONE_LEN = 15

# Websocket
OLD_MESSAGES_TO_LOAD = (
    30  # limit the amount of messages history to load on each chat connection
)

# getting users in range
USERS_RANGE = 50  # in meters
