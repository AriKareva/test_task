from backend.task.schemas import TaskCreate, TaskUpdate
from sqlalchemy import select
from models import Task
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.task_id == task_id)
        result = await self.db.execute(query)
        task =  result.scalar_one_or_none()
        return task

    async def list(self) -> list[Task]| None:
        query = select(Task)
        result = await self.db.execute(query)
        task = result.scalars().all()
        return task

    async def create(self, data: TaskCreate) -> Task:
        new_task = Task(**data.model_dump())
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def delete(self, task_id: int) -> Task | None:
        task = await self.get(task_id=task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
            return task
        return None

    def update(self, updates: TaskUpdate):
        ...

