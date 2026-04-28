from typing import List
from task.schemas import TaskCreate, TaskUpdate
from task.models import Task, TaskAssignee
from sqlalchemy import func
from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int) -> Task | None:
        task = self.db.query(Task).filter(Task.task_id == task_id).first()
        return task

    def list(self) -> List[Task]:
        tasks = self.db.query(Task).all()
        return tasks
    
    def user_created_list(self, user_id: int) -> List[Task]:
        user_tasks = self.db.query(Task).filter(Task.author_id == user_id).all()
        return user_tasks
    
    def user_assigned_list(self, assignee_id: int) -> List[Task]:
        latest_assignee_ids = (
            self.db.query(
                TaskAssignee.task_id,
                func.max(TaskAssignee.task_assignee_id).label('max_id')
            )
            .group_by(TaskAssignee.task_id)
            .subquery()
        )

        user_tasks = (
            self.db.query(Task)
            .join(TaskAssignee, Task.task_id == TaskAssignee.task_id)
            .join(
                latest_assignee_ids,
                TaskAssignee.task_assignee_id == latest_assignee_ids.c.max_id
            )
            .filter(TaskAssignee.assignee_id == assignee_id)
            .all()
        )
        return user_tasks

    def create(self, data: TaskCreate, author_id: int) -> Task:
        new_task = Task(**data.model_dump())
        setattr(new_task, 'author_id', author_id)
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def delete(self, task_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return task
        return None

    def update(self, task_id: int, updates: TaskUpdate) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None

        for k, v in updates.model_dump(exclude_unset=True).items():
            setattr(task, k, v)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_assignee(self, task_id: int, new_assignee_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None
        
        new_assignment = TaskAssignee(
            task_id=task_id,
            assignee_id=new_assignee_id,
        )

        self.db.add(new_assignment)
        self.db.commit()
        self.db.refresh(task)
        return task