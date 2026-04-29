from typing import Any, List
from user.schemas import AccessTokenPayload
from dependencies import get_current_user, get_task_manager
from task.schemas import ( 
    TaskFullCreate, TaskFullResponse, PriorityResponse, 
    StatusResponse, TaskResponse, TaskStatusResponse, 
    TaskPriorityResponse, TaskAssigneeUpdate,
    StatusUpdate, PriorityUpdate
)
from task.task_manager import TaskManager
from fastapi import APIRouter, Depends


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/statuses', response_model=List[StatusResponse])
def get_statuses(manager: TaskManager = Depends(get_task_manager)):
    return manager.get_statuses()

@router.get('/priorities', response_model=List[PriorityResponse])
def get_priorities(manager: TaskManager = Depends(get_task_manager)):
    return manager.get_priorities()

@router.get('/', response_model=List[TaskFullResponse])
def get_tasks(
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.list_tasks()

@router.get('/{task_id}', response_model=TaskFullResponse)
def get_task(
    task_id: int,
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.get_task(task_id=task_id)
    
@router.post('/', response_model=TaskFullResponse)
def create_task(
    task_data: TaskFullCreate,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.create_task(task_data=task_data, author_id=cur_user.user_id)

@router.patch('/{task_id}/priority', response_model=TaskFullResponse)
def update_task_prtiority(
    new_prtiority: PriorityUpdate,
    task_id: int,
    # user_id: int,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_priority(task_id=task_id, priority_id=new_prtiority.priority_id, user_id=cur_user.user_id)

@router.patch('/{task_id}/assignee', response_model=TaskResponse)
def update_task_assignee(
    assignee: TaskAssigneeUpdate,
    task_id: int,
    # user_id: int,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_assignee(task_id=task_id, new_assignee_id=assignee.assignee_id, user_id=cur_user.user_id)

@router.patch('/{task_id}/status', response_model=TaskFullResponse)
def update_task_status(
    new_status: StatusUpdate,
    task_id: int,
    # user_id: int,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_status(task_id=task_id, new_status_id=new_status.status_id, user_id=cur_user.user_id)

@router.delete('/{task_id}', response_model=TaskFullResponse)
def delete_task(
    task_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.delete_task(task_id=task_id)


@router.get('/{user_id}/created', response_model=List[TaskFullResponse])
def list_user_created_tasks(
    user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.list_user_created_tasks(user_id=user_id)


@router.get('/{user_id}/assigned', response_model=List[TaskFullResponse])
def list_user_assigned_tasks(
    user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.list_user_assigned_tasks(assignee_id=user_id)


@router.get('/{task_id}/status-history', response_model=List[TaskStatusResponse])
def get_task_status_history(task_id: int, manager: TaskManager = Depends(get_task_manager)):
    return manager.get_status_history(task_id)

@router.get('/{task_id}/priority-history', response_model=List[TaskPriorityResponse])
def get_task_priority_history(task_id: int, manager: TaskManager = Depends(get_task_manager)):
    return manager.get_priority_history(task_id)