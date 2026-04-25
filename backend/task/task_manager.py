from typing import List
from task.schemas import TaskResponse, TaskUpdate, TaskCreate
from task.task_repository import TaskRepository
from fastapi import HTTPException, status


class TaskManager:
    def __init__(self, rep: TaskRepository):
        self.rep = rep

    def get_task(self, task_id: int) -> TaskResponse:
        task = self.rep.get(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return task

    def list_tasks(self) -> List[TaskResponse]:
        tasks = self.rep.list()
        return tasks

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        new_task = self.rep.create(data=task_data)
        return new_task

    def delete_task(self, task_id: int) -> TaskResponse:
        deleted_task = self.rep.delete(task_id=task_id)
        if not deleted_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return deleted_task

    def update_task(self, task_id: int, task_updates: TaskUpdate) -> TaskResponse:
        updated_task = self.rep.update(task_id=task_id, updates=task_updates)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return updated_task


