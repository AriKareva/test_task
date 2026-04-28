from typing import List
from user.models import User
from user.auth.password_manager import verify_password
from user.auth.jwt_tokens_manager import create_access_token
from user.user_repository import UserRepository
from user.schemas import AccessTokenResponse, UserCreate, UserSignIn, UserUpdate
from fastapi import HTTPException, status


class UserManager:
    def __init__(self, rep: UserRepository):
        self.rep = rep

    def get_user(self, user_id: int) -> User:
        task = self.rep.get(user_id=user_id)
        if not task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return task

    def list_users(self) -> List[User]:
        users = self.rep.list()
        return users

    def create_user(self, user_data: UserCreate) -> User:
        user_exists = self.rep.get_user_by_login(user_login=user_data.login)
        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Пользователь с login={user_data.login} уже существует')
       
        user_exists = self.rep.get_user_by_email(user_email=user_data.email)
        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Пользователь с email={user_data.email} уже существует')
        
        new_task = self.rep.create(data=user_data)
        return new_task

    def delete_user(self, user_id: int) -> User:
        deleted_task = self.rep.delete(user_id=user_id)
        if not deleted_task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return deleted_task

    def update_user(self, user_id: int, user_updates: UserUpdate) -> User:
        updated_task = self.rep.update(user_id=user_id, updates=user_updates)
        if not updated_task:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с id={user_id} не найден')
        return updated_task

    def signin(self, user_data: UserSignIn) -> AccessTokenResponse:
        user = self.rep.get_user_by_login(user_login=user_data.login)
        if not user:
            raise HTTPException(status_code=status.HTTH_404_NOT_FOUND, detail=f'Пользователь с login={user_data.login} не найден')
        
        pass_verified = verify_password(user_data.password, user.password)
        if not pass_verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный пароль')
        
        token = create_access_token(user_id=user.user_id, login=user.login)
        return token

        
