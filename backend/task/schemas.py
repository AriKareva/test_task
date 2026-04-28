from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TaskAssigneeBase(BaseModel):
    task_id: int 
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskAssigneeCreate(TaskAssigneeBase):
    ...


class TaskAssigneeUpdate(TaskAssigneeBase):
    ...


class TaskAssigneeResponse(TaskAssigneeBase):
    task_assignee_id: int
    assignee_dt: datetime



class TaskBase(BaseModel):
    task_title: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    ...


class TaskUpdate(TaskBase):
    ...


class TaskResponse(TaskBase):
    task_id: int
    cur_assignee: Optional[TaskAssigneeResponse] = None
    current_status: str = 'Создана'
