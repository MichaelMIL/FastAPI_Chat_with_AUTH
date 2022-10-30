from typing import List
from fastapi import APIRouter, Request, Depends
from models.user import User


router = APIRouter()


@router.get('/user', response_model=User)
def get_current_user(current_user: User = Depends(get_current_active_user))
    return current_user.dict()