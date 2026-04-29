from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TaskAssigneeBase(BaseModel):
    assignee_id: Optional[int] = None
    assignee_login: Optional[str] = None

    class Config:
        from_attributes = True

class TaskAssigneeCreate(TaskAssigneeBase):
    ...

class TaskAssigneeUpdate(TaskAssigneeBase):
    ...

class TaskAssigneeResponse(TaskAssigneeBase):
    assignee_dt: datetime


class TaskStatusBase(BaseModel):
    status_id: int 
    status_title: str

    class Config:
        from_attributes = True

class TaskStatusCreate(TaskStatusBase):
    ...

class TaskStatusUpdate(TaskStatusBase):
    ...

class TaskStatusResponse(TaskStatusBase):
    status_dt: datetime


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

class TaskFullResponse(TaskBase):
    task_id: int
    cur_assignee: Optional[TaskAssigneeResponse] = None
    current_status: Optional[TaskStatusResponse] = None
