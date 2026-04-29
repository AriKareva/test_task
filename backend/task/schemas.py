from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PriorityBase(BaseModel):
    priority_id: int
    priority_title: str

    class Config:
        from_attributes = True

class PriorityUpdate(BaseModel):
    priority_id: int

class PriorityResponse(PriorityBase):
    ...


class TaskAssigneeBase(BaseModel):
    assignee_id: Optional[int] = None
    assignee_login: Optional[str] = None

    class Config:
        from_attributes = True

class TaskAssigneeUpdate(BaseModel):
    assignee_id: int

class TaskAssigneeResponse(TaskAssigneeBase):
    assignee_dt: datetime


class StatusBase(BaseModel):
    status_id: int 
    status_title: str
    
    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status_id: int

class StatusResponse(StatusBase):
    ...


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

    class Config:
        from_attributes = True

class TaskCreate(TaskBase):
    ...

class TaskUpdate(TaskBase):
    ...

class TaskResponse(TaskBase):
    task_id: int
    author_id: Optional[int] = None
    cur_assignee: Optional[TaskAssigneeResponse] = None
    current_status: Optional[TaskStatusResponse] = None


class TaskFullBase(BaseModel):
    task_id: int
    task_title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    author_id: int
    author_login: str
    cur_assignee: Optional[TaskAssigneeResponse] = None
    current_status: TaskStatusResponse

    class Config:
        from_attributes = True


class TaskFullResponse(TaskFullBase):
    ...


class TaskPriorityBase(BaseModel):
  priority_id: int
  priority_title: str
  priority_dt: datetime

class TaskPriorityResponse(TaskPriorityBase):
    ...