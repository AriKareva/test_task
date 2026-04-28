from user.auth.password_manager import hash_password
from user.models import User
from user.schemas import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        query = select(User).where(User.user_id == user_id)
        result = self.db.execute(query)
        task =  result.scalar_one_or_none()
        return task

    def list(self) -> list[User]:
        query = select(User)
        result = self.db.execute(query)
        task = result.scalars().all()
        return task

    def create(self, data: UserCreate) -> User:
        hashed_password = hash_password(data.password)
        new_user = User(
            login=data.login,
            password=hashed_password, 
            email=data.email
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def delete(self, user_id: int) -> User | None:
        task = self.get(user_id=user_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return task
        return None

    def update(self, user_id: int, updates: UserUpdate) -> User | None:
        task = self.get(user_id=user_id)
        if not task:
            return None

        for k, v in updates.model_dump(exclude_unset=True).items():
            setattr(task, k, v)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_user_by_login(self, user_login: str) -> User | None:
        user = self.db.query(User).filter(User.login == user_login).first()
        return user
    
    def get_user_by_email(self, user_email: str) -> User | None:
        user = self.db.query(User).filter(User.email == user_email).first()
        return user
    
