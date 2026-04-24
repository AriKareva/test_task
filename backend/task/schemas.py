from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    ...

class TaskCreate(TaskBase):
    task_title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    author_id: int
    assignee_id: int

    class Config:
        from_attributes = True

class TaskUpdate(TaskBase):
    task_title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    author_id: Optional[int] = None
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True