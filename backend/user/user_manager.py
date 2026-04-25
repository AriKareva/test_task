from typing import List
from user.user_repository import UserRepository
from user.schemas import UserCreate, UserResponse, UserUpdate
from fastapi import HTTPException, status


class UserManager:
    def __init__(self, rep: UserRepository):
        self.rep = rep

    def get_user(self, user_id: int) -> UserResponse:
        task = self.rep.get(user_id=user_id)
        if not task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return task

    def list_users(self) -> List[UserResponse]:
        users = self.rep.list()
        return users

    def create_user(self, user_data: UserCreate) -> UserResponse:
        new_task = self.rep.create(data=user_data)
        return new_task

    def delete_user(self, user_id: int) -> UserResponse:
        deleted_task = self.rep.delete(user_id=user_id)
        if not deleted_task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return deleted_task

    def update_user(self, user_id: int, user_updates: UserUpdate) -> UserResponse:
        updated_task = self.rep.update(user_id=user_id, updates=user_updates)
        if not updated_task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return updated_task


