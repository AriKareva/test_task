from user.auth.jwt_tokens_manager import decode_access_token
from user.schemas import AccessTokenPayload
from task.task_repository import TaskRepository
from user.user_repository import UserRepository
from database.connection import SessionLocal
from user.user_manager import UserManager
from task.task_manager import TaskManager
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer


def get_db() -> Session:
    with SessionLocal() as db:
        yield db

def get_task_manager(db: Session = Depends(get_db)) -> TaskManager:
    rep = TaskRepository(db)
    return TaskManager(rep)

def get_user_manager(db: Session = Depends(get_db)) -> UserManager:
    rep = UserRepository(db)
    return UserManager(rep)

bearer = HTTPBearer()

def get_current_user(credentials = Depends(bearer)) -> AccessTokenPayload:
    token = credentials.credentials
    token_payload = decode_access_token(token)
    
    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный или истёкший токен',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_payload
