from task.models import Task
from typing import Any, List
from task.schemas import PriorityResponse, TaskFullCreate, TaskFullResponse, TaskPriorityResponse, TaskStatusResponse, TaskUpdate, TaskCreate, StatusResponse
from task.task_repository import TaskRepository
from fastapi import HTTPException, status


class TaskManager:
    def __init__(self, rep: TaskRepository):
        self.rep = rep

    def get_task(self, task_id: int) -> TaskFullResponse:
        task = self.rep.get(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return task

    def list_tasks(self) -> List[TaskFullResponse]:
        tasks = self.rep.list()
        return tasks

    def list_user_assigned_tasks(self, assignee_id: int) -> List[TaskFullResponse]:
        tasks = self.rep.user_assigned_list(assignee_id=assignee_id)
        return tasks
    
    def list_user_created_tasks(self, user_id: int) -> List[TaskFullResponse]:
        tasks = self.rep.user_created_list(user_id=user_id)
        return tasks

    def create_task(self, task_data: TaskFullCreate, author_id: int) -> TaskFullResponse:
        new_task = self.rep.create(data=task_data, author_id=author_id)
        return new_task

    def delete_task(self, task_id: int) -> Task:
        task = self.rep.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        self.rep.delete(task_id)
        return task
    
    def update_task(self, task_id: int, task_updates: TaskUpdate) -> Task:
        updated_task = self.rep.update(task_id=task_id, updates=task_updates)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        return updated_task
    
    def _assignee_exists(self, assignee: str) -> int | None:
        return self.rep.get_assignee_by_name(assignee_name=assignee)
    
    def get_task_assignee_id(self, task_id: int) -> int | None:
        return self.rep.get_cur_task_assignee_id(task_id=task_id)

    def update_task_assignee(self, task_id: int, new_assignee_id: int, user_id: int) -> TaskFullResponse:
        task_author_id = self.rep.get(task_id=task_id).author_id
        if not task_author_id == user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Вы не можете изменить исполниителя задачи, автором которой не являетесь')

        updated_task = self.rep.update_assignee(task_id=task_id,new_assignee_id=new_assignee_id)
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Задача с id={task_id} не найдена')
        
        return updated_task
    
    def _priority_exists(self, priority: str) -> int | None:
        return self.rep.get_priority_by_name(priority_name=priority)
    
    def update_task_priority(self, task_id: int, priority_id: int,
                            user_id: int) -> TaskFullResponse:
        task = self.rep.get(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Задача не найдена')

        # Только автор может менять приоритет
        # if task.author_id != user_id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        #                         detail='Только автор может изменить приоритет')

        updated_task = self.rep.update_priority(task_id=task_id,
                                                priority_id=priority_id)
        return updated_task
    
    def _status_exists(self, status: str) -> int | None:
        return self.rep.get_status_by_name(status_name=status)
    
    def update_task_status(self, task_id: int, new_status_id: int, user_id: int) -> TaskFullResponse:
        task = self.rep.get(task_id=task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Задача не найдена')

        # автор или текущий исполнитель могут менять статус
        current_assignee_id = self.get_task_assignee_id(task_id=task_id)
        # if task.author_id != user_id and current_assignee_id != user_id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        #                         detail='У вас нет прав на изменение статуса')

        updated_task = self.rep.update_status(task_id=task_id,
                                            new_status_id=new_status_id)
        return updated_task

    def get_statuses(self) -> List[StatusResponse]:
        statuses = self.rep.get_statuses()
        return [StatusResponse.model_validate(s) for s in statuses]

    def get_priorities(self) -> List[PriorityResponse]:
        return self.rep.get_priorities()

    def get_status_history(self, task_id: int) -> List[TaskStatusResponse]:
        return self.rep.get_status_history(task_id)

    def get_priority_history(self, task_id: int) -> List[TaskPriorityResponse]:
        return self.rep.get_priority_history(task_id)