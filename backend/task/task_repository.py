from typing import Any, List, Optional
from user.models import User
from task.schemas import PriorityResponse, TaskAssigneeResponse, TaskCreate, TaskPriorityResponse, TaskStatusResponse, TaskUpdate, TaskFullResponse
from task.models import Priority, Status, Task, TaskAssignee, TaskPriority, TaskStatus
from sqlalchemy import func
from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int) -> Task | None:
        task = self.db.query(Task).filter(Task.task_id == task_id).first()
        return task

    def get_cur_task_assignee_id(self, task_id: int) -> int | None:
        latest_assignee = (
            self.db.query(TaskAssignee)
            .filter(TaskAssignee.task_id == task_id)
            .order_by(TaskAssignee.task_assignee_id.desc())
            .first()
        )
        if not latest_assignee:
            return None
        
        return latest_assignee.assignee_id

    def get_current_assignee(self, task_id: int) -> Optional[TaskAssigneeResponse]:
        row = (
            self.db.query(TaskAssignee.assignee_id, User.login, TaskAssignee.assignee_dt)
            .join(User, TaskAssignee.assignee_id == User.user_id)
            .filter(TaskAssignee.task_id == task_id)
            .order_by(TaskAssignee.task_assignee_id.desc())
            .first()
        )
        if not row:
            return None
        assignee_id, login, assignee_dt = row
        return TaskAssigneeResponse(
            assignee_id=assignee_id,
            assignee_login=login,
            assignee_dt=assignee_dt
        )

    def get_current_status(self, task_id: int) -> Optional[TaskStatusResponse]:
        row = (
            self.db.query(TaskStatus.status_id, Status.status_title, TaskStatus.status_dt)
            .join(Status, TaskStatus.status_id == Status.status_id)
            .filter(TaskStatus.task_id == task_id)
            .order_by(TaskStatus.task_status_id.desc())
            .first()
        )
        if not row:
            return None
        status_id, status_title, status_dt = row
        return TaskStatusResponse(
            status_id=status_id,
            status_title=status_title,
            status_dt=status_dt
        )

    def list(self, assignee_id: Optional[int] = None, author_id: Optional[int] = None) -> List[TaskFullResponse]:
        latest_assignee_subq = (
            self.db.query(
                TaskAssignee.task_id,
                func.max(TaskAssignee.task_assignee_id).label('max_id')
            )
            .group_by(TaskAssignee.task_id)
            .subquery()
        )
        if assignee_id:
            task_ids = (
                self.db.query(TaskAssignee.task_id)
                .join(
                    latest_assignee_subq,
                    TaskAssignee.task_assignee_id == latest_assignee_subq.c.max_id
                )
                .filter(TaskAssignee.assignee_id == assignee_id)
                .all()
            )
        else:
            task_ids = (
                self.db.query(TaskAssignee.task_id)
                .join(
                    latest_assignee_subq,
                    TaskAssignee.task_assignee_id == latest_assignee_subq.c.max_id
                )
                .all()
            )

        task_ids = [t[0] for t in task_ids]
        if not task_ids:
            return []
        
        tasks = self.db.query(Task).filter(Task.task_id.in_(task_ids)).all()
        
        result = []
         
        for task in tasks:
            author = self.db.query(User).filter(User.user_id == task.author_id).first()
            author_login = author.login
            
            result.append(TaskFullResponse(
                task_id=task.task_id,
                task_title=task.task_title,
                description=task.description,
                author_id=task.author_id,
                author_login=author_login,
                cur_assignee=self.get_current_assignee(task.task_id),
                current_status=self.get_current_status(task.task_id),
                deadline=task.deadline
            ))
        return result

    def user_created_list(self, user_id: int) -> List[TaskFullResponse]:
        user_tasks = self.list(author_id=user_id)
        return user_tasks
    
    def user_assigned_list(self, assignee_id: int) -> List[TaskFullResponse]:
        assignee_tasks = self.list(assignee_id=assignee_id)
        return assignee_tasks

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

    def get_priority_by_name(self, priority_name: str) -> int | None:
        priority = self.db.query(Priority).filter(Priority.priority_title == priority_name).first()
        if not priority:
            return None
        
        return priority.priority_id
    
    def update_priority(self, task_id: int, new_priority_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None
        
        new_priority = TaskPriority(
            task_id=task_id,
            priority_id=new_priority_id
        )

        self.db.add(new_priority)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_status(self, task_id: int, new_status_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None
        
        new_status = TaskStatus(
            task_id=task_id,
            status_id=new_status_id
        )

        self.db.add(new_status)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_status_by_name(self, status_name: str) -> int | None:
        status = self.db.query(Status).filter(Status.status_title == status_name).first()
        if not status:
            return None
        
        return status.status_id

    def update_assignee(self, task_id: int, new_assignee_id: int) -> Task | None:
        task = self.get(task_id=task_id)
        if not task:
            return None
        
        new_assignee = TaskAssignee(
            task_id=task_id,
            assignee_id=new_assignee_id
        )

        self.db.add(new_assignee)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_assignee_by_name(self, assignee_name: str) -> int | None:
        assignee = self.db.query(User).filter(User.login == assignee_name).first()
        if not assignee:
            return None
        
        return assignee.user_id
    
    def get_statuses(self) -> List[Status]: 
        statuses = self.db.query(Status).all()
        return statuses
    
    def get_priorities(self) -> List[PriorityResponse]:
        priorities = self.db.query(Priority).all()
        return [PriorityResponse.model_validate(p) for p in priorities]

    def get_status_history(self, task_id: int) -> List[TaskStatusResponse]:
        rows = (
            self.db.query(TaskStatus, Status.status_title)
            .join(Status, TaskStatus.status_id == Status.status_id)
            .filter(TaskStatus.task_id == task_id)
            .order_by(TaskStatus.status_dt.desc())
            .all()
        )
        return [
            TaskStatusResponse(
                status_id=ts.status_id,
                status_title=title,
                status_dt=ts.status_dt
            )
            for ts, title in rows
        ]

    def get_priority_history(self, task_id: int) -> List[TaskPriorityResponse]:
        rows = (
            self.db.query(TaskPriority, Priority.priority_title)
            .join(Priority, TaskPriority.priority_id == Priority.priority_id)
            .filter(TaskPriority.task_id == task_id)
            .order_by(TaskPriority.priority_dt.desc())
            .all()
        )
        return [
            TaskPriorityResponse(
                priority_id=tp.priority_id,
                priority_title=title,
                priority_dt=tp.priority_dt
            )
            for tp, title in rows
        ]