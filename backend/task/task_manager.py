from task.models import Task
from typing import List
from task.schemas import TaskUpdate, TaskCreate
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

    def list_user_assigned_tasks(self, assignee_id: int) -> List[Task]:
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

    def update_task_assignee(self, task_id: int, new_assignee_id: int) -> Task:
        updated_task = self.rep.update_assignee(task_id=task_id, new_assignee_id=new_assignee_id)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return updated_task

