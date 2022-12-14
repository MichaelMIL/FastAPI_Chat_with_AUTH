from typing import List, Union
from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Request,
    Depends,
    UploadFile,
    Response,
)
from actions.auth_actions import verify_jwt_token
from configs import USERS_RANGE
from lib.s3.bucket import S3_Bucket
from models.auth_model import Token
from models.user_model import CreateUser, UpdateUser, User
from actions.user_actions import (
    _create_user,
    _delete_user,
    _get_user,
    _get_user_by_phone,
    _get_users_in_range,
    _update_user,
)

user_router = APIRouter()


@user_router.post("/", response_model=User)
async def create_user(
    request: Request,
    user: CreateUser = Body(...),
    token: Token = Depends(verify_jwt_token),
):
    user = _create_user(request=request, user=user)
    return user


@user_router.get("/{UserId}", response_model=User)
async def get_user(
    request: Request, UserId: str, token: Token = Depends(verify_jwt_token)
):
    user = _get_user(request=request, user_id=UserId)
    return user


@user_router.get("/phone/{UserPhoneNumber}", response_model=User)
async def get_user_by_phone(
    request: Request, UserPhoneNumber: str, token: Token = Depends(verify_jwt_token)
):
    user = _get_user_by_phone(request=request, user_phone=UserPhoneNumber)
    return user


@user_router.delete("/", response_model=None)
async def delete_user(request: Request, token: Token = Depends(verify_jwt_token)):
    _delete_user(request=request, user_id=token["id"])


@user_router.put("/", response_model=dict)
async def update_user(
    request: Request,
    user: UpdateUser = Body(...),
    token: Token = Depends(verify_jwt_token),
):
    user = user.dict()
    _ = user.copy()
    for item, value in _.items():
        if not value:
            del user[item]
    updated_user = _update_user(request=request, user_id=token["id"], user=user)
    return updated_user


@user_router.put("/set-location/{Lat}/{Lon}", response_model=dict)
async def update_user_location(
    request: Request,
    Lat: Union[str, int, float],
    Lon: Union[str, int, float],
    token: Token = Depends(verify_jwt_token),
):
    return await update_user(
        request=request,
        UserId=token["id"],
        user={"user_location": {"lat": str(Lat), "lon": str(Lon)}},
        token=token,
    )


@user_router.get("/location/in-range", response_model=List[User])
async def get_users_in_range(
    request: Request, token: Token = Depends(verify_jwt_token)
):
    return _get_users_in_range(request=request, user_id=token["id"], range=USERS_RANGE)


@user_router.post("/picture/profile")
async def upload_profile_picture_for_current_user_JPG_ONLY(
    request: Request, file: UploadFile, token: Token = Depends(verify_jwt_token)
):
    user_id = token["id"]
    bucket: S3_Bucket = request.app.s3_bucket
    data = await file.read()
    return bucket.upload_file(user_id + ".jpg", data)


@user_router.get("/picture/profile/{User_Id}")
async def get_profile_picture_for_user(
    request: Request, UserId: str, token: Token = Depends(verify_jwt_token)
):
    bucket: S3_Bucket = request.app.s3_bucket
    out = bucket.download_file(UserId + ".jpg")
    return Response(content=out, media_type="image/png")
