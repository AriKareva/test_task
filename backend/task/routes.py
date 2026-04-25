from typing import List
from dependencies import get_task_manager
from task.schemas import TaskCreate, TaskResponse, TaskUpdate
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
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.create_task(task_data=task_data)

@router.patch('/{task_id}', response_model=TaskResponse)
def update_task(
    updates: TaskUpdate,
    task_id: int,
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.update_task(task_id=task_id, task_updates=updates)

@router.delete('/{task_id}', response_model=TaskResponse)
def delete_task(
    task_id: int,
    # user_id: int,
    manager: TaskManager = Depends(get_task_manager)
):
    return manager.delete_task(task_id=task_id)