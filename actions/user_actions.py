from typing import List
from lib.dynamo_db.table import DynamoTable
from fastapi import HTTPException, Request
from models.user_model import CreateUser, User
from math import sin, cos, sqrt, atan2, radians


def _create_user(request: Request, user: CreateUser) -> User:
    table: DynamoTable = request.app.users_table
    db_user = table.query_items("phone", str(user.phone), "phone-index")
    if db_user:
        raise HTTPException(409, f"User with phone {user.phone} already exists!")
    table.add_item(user.dict())
    return User(**user.dict())


def _get_user(request: Request, user_id: str) -> User:
    table: DynamoTable = request.app.users_table
    user = table.query_items("id", user_id)
    if not len(user) > 0:
        raise HTTPException(404, f"User not found ({user_id})")
    return User(**user[0])


def _get_user_by_phone(request: Request, user_phone: str) -> User:
    table: DynamoTable = request.app.users_table
    user = table.query_items("phone", str(user_phone), "phone-index")
    if not len(user) > 0:
        raise HTTPException(404, f"User not found ({user_phone})")
    return User(**user[0])


def _delete_user(request: Request, user_id: str) -> None:
    table: DynamoTable = request.app.users_table
    table.delete_item({"id": user_id})


def _update_user(request: Request, user_id: str, user: dict) -> dict:
    table: DynamoTable = request.app.users_table
    updated_user = table.update_item_by_dict(key={"id": user_id}, dict=user)
    if not updated_user:
        raise HTTPException(400, "Missing body")
    return updated_user


def _get_users_in_range(request: Request, user_id: str, range: float = 50) -> List:
    table: DynamoTable = request.app.users_table
    current_user = _get_user(request, user_id)
    users = table.get_all_items()
    out = []
    for user in users:
        if (
            distance_between_coordinates(
                lat1=float(current_user.user_location["lat"]),
                lon1=float(current_user.user_location["lon"]),
                lat2=float(user["user_location"]["lat"]),
                lon2=float(user["user_location"]["lon"]),
            )
            <= range
        ):
            out.append(user)
    return out


def distance_between_coordinates(
    lat1: float, lon1: float, lat2: float, lon2: float, earth_radius=6373.0
) -> float:
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c * 1000
