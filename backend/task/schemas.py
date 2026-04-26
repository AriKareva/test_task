from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    task_title: str


class TaskUpdate(TaskBase):
    task_title: Optional[str] = None



class TaskResponse(TaskBase):
    task_id: int
    task_title: Optional[str] = None
