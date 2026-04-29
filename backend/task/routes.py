from typing import List
from user.schemas import AccessTokenPayload
from dependencies import get_current_user, get_task_manager
from task.schemas import TaskCreate, TaskFullResponse, TaskResponse, TaskUpdate
from task.task_manager import TaskManager
from fastapi import APIRouter, Depends


router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', response_model=List[TaskResponse])
def get_tasks(
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.list_tasks()

@router.get('/{task_id}', response_model=TaskResponse)
def get_task(
    task_id: int,
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.get_task(task_id=task_id)
    

@router.post('/', response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.create_task(task_data=task_data, author_id=cur_user.user_id)


@router.patch('/{task_id}/priority', response_model=TaskResponse)
def update_task_prtiority(
    new_prtiority: str,
    task_id: int,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_priority(task_id=task_id, new_priority=new_prtiority)

@router.patch('/{task_id}/assignee', response_model=TaskResponse)
def update_task_assignee(
    new_assignee: str,
    task_id: int,
    cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_assignee(task_id=task_id, new_assignee=new_assignee, user_id=cur_user.user_id)

@router.patch('/{task_id}/status', response_model=TaskResponse)
def update_task_status(
    new_status: str,
    task_id: int,
    # cur_user: AccessTokenPayload = Depends(get_current_user),
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task_status(task_id=task_id, new_status=new_status)


@router.delete('/{task_id}', response_model=TaskResponse)
def delete_task(
    task_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.delete_task(task_id=task_id)


@router.get('/{user_id}/created', response_model=List[TaskResponse])
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
