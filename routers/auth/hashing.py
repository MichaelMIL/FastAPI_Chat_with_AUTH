import hashlib


def hash_password(password: str, username: str):
    salt = str(username)
    to_hash = salt + str(password)
    return hashlib.sha256(to_hash.encode()).hexdigest()


def verify_password(password: str, username: str, hashed_password: str):
    return hash_password(password, username) == hashed_password


def calculate_bytes_checksum(bytes):
    return hashlib.sha256(bytes).hexdigest()


def calculate_file_checksum(file_path):
    with open(file_path, "rb") as f:
        return calculate_bytes_checksum(f.read())
