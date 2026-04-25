from task.schemas import TaskCreate, TaskUpdate
from task.models import Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.task_id == task_id)
        result = self.db.execute(query)
        task =  result.scalar_one_or_none()
        return task

    def list(self) -> list[Task]:
        query = select(Task)
        result = self.db.execute(query)
        task = result.scalars().all()
        return task

    def create(self, data: TaskCreate) -> Task:
        new_task = Task(**data.model_dump())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def delete(self, task_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return task
        return None

    def update(self, task_id: int, updates: TaskUpdate) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None

        for k, v in updates.model_dump(exclude_unset=True).items():
            setattr(task, k, v)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

