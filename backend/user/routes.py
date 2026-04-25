from typing import List
from user.user_manager import UserManager
from user.schemas import UserCreate, UserResponse, UserUpdate
from dependencies import get_user_manager
from fastapi import APIRouter, Depends


router = APIRouter(prefix='/user', tags=['user'])

@router.get('/', response_model=List[UserResponse])
def get_tasks(
    # user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.list_users()

@router.get('/{task_id}', response_model=UserResponse)
def get_task(
    user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.get_user(user_id=user_id)
    

@router.post('/', response_model=UserResponse)
def create_task(
    user_data: UserCreate,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.create_user(user_data=user_data)


@router.patch('/{task_id}', response_model=UserResponse)
def update_task(
    updates: UserUpdate,
    user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.update_user(user_id=user_id, user_updates=updates)


@router.delete('/{task_id}', response_model=UserResponse)
def delete_task(
    user_id: int,
    manager: UserManager = Depends(get_user_manager)
):
    return manager.delete_user(user_id=user_id)