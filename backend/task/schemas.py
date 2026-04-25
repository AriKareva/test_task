from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    description: Optional[str] = None
    priority: Optional[int] = None
    assignee_id: Optional[int] = None

class TaskCreate(TaskBase):
    task_title: str
    author_id: int

    class Config:
        from_attributes = True

class TaskUpdate(TaskBase):
    task_title: Optional[str] = None

    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    task_title: Optional[str] = None

    class Config:
        from_attributes = True