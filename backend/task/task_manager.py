from task.models import Task
from typing import List
from task.schemas import TaskFullResponse, TaskUpdate, TaskCreate
from task.task_repository import TaskRepository
from fastapi import HTTPException, status


class TaskManager:
    def __init__(self, rep: TaskRepository):
        self.rep = rep

    def get_task(self, task_id: int) -> Task:
        task = self.rep.get(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return task

    def list_tasks(self) -> List[Task]:
        tasks = self.rep.list()
        return tasks

    def list_user_assigned_tasks(self, assignee_id: int) -> List[TaskFullResponse]:
        tasks = self.rep.user_assigned_list(assignee_id=assignee_id)
        return tasks
    
    def list_user_created_tasks(self, user_id: int) -> List[Task]:
        tasks = self.rep.user_created_list(user_id=user_id)
        return tasks

    def create_task(self, task_data: TaskCreate, author_id: int) -> Task:
        new_task = self.rep.create(data=task_data, author_id=author_id)
        return new_task

    def delete_task(self, task_id: int) -> Task:
        deleted_task = self.rep.delete(task_id=task_id)
        if not deleted_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return deleted_task

    def update_task(self, task_id: int, task_updates: TaskUpdate) -> Task:
        updated_task = self.rep.update(task_id=task_id, updates=task_updates)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return updated_task
    
    def _assignee_exists(self, assignee: str) -> int | None:
        return self.rep.get_assignee_by_name(assignee_name=assignee)
    
    def update_task_assignee(self, task_id: int, new_assignee: str, user_id: int) -> Task:
        task_author_id = self.rep.get(task_id=task_id)
        # if not task_author_id == user_id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Вы не можете изменить исполниителя задачи, автором которой не являетесь')
        
        new_assignee_id = self._assignee_exists(assignee=new_assignee)
        if not new_assignee_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Пользователь {new_assignee} с id={new_assignee_id} не найден')
        
        updated_task = self.rep.update_assignee(task_id=task_id,new_assignee_id=new_assignee_id)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        
        return updated_task
    
    def _priority_exists(self, priority: str) -> int | None:
        return self.rep.get_priority_by_name(priority_name=priority)
    
    def update_task_priority(self, task_id: int, new_priority: str) -> Task:
        new_priority_id = self._priority_exists(priority=new_priority)
        if not new_priority_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Неизвестный приоритет задачи {new_priority}')
        
        updated_task = self.rep.update_priority(task_id=task_id, new_priority_id=new_priority_id)
        
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        
        return updated_task
    
    def _status_exists(self, status: str) -> int | None:
        return self.rep.get_status_by_name(status_name=status)
    
    def update_task_status(self, task_id: int, new_status: str) -> Task:
        new_status_id = self._status_exists(status=new_status)
        if not new_status_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Неизвестный статус задачи {new_status}')
        
        updated_task = self.rep.update_status(task_id=task_id, new_status_id=new_status_id)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        
        return updated_task

