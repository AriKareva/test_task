from task.task_repository import TaskRepository
from user.user_repository import UserRepository
from database.connection import SessionLocal
from user.user_manager import UserManager
from task.task_manager import TaskManager
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db() -> Session:
    with SessionLocal() as db:
        yield db

def get_task_manager(db: Session = Depends(get_db)) -> TaskManager:
    rep = TaskRepository(db)
    return TaskManager(rep)

async def get_user_manager(db: Session = Depends(get_db)) -> UserManager:
    rep = UserRepository(db)
    return UserManager(rep)