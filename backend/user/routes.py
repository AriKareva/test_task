from typing import List
from user.user_manager import UserManager
from user.schemas import AccessTokenPayload, AccessTokenResponse, UserCreate, UserResponse, UserSignIn, UserUpdate
from dependencies import get_current_user, get_user_manager
from fastapi import APIRouter, Depends


router = APIRouter(prefix='/user', tags=['user'])

@router.get('/', response_model=List[UserResponse])
def get_users(
    manager: UserManager = Depends(get_user_manager)
):
    return manager.list_users()

@router.get('/{user_id}', response_model=UserResponse)
def get_user(
    user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.get_user(user_id=user_id)
    

@router.post('/', response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.create_user(user_data=user_data)


@router.patch('/', response_model=UserResponse)
def update_user(
    updates: UserUpdate,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
):
    return manager.update_user(user_id=cur_user.user_id, user_updates=updates)


@router.delete('/{user_id}', response_model=UserResponse)
def delete_user(
    user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.delete_user(user_id=user_id)


@router.post('/signin', response_model=AccessTokenResponse)
def signin(
    user_data: UserSignIn,
    manager: UserManager = Depends(get_user_manager)
):
           
    return manager.signin(user_data=user_data)
