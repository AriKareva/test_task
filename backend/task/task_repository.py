from typing import List
from user.models import User
from task.schemas import TaskAssigneeResponse, TaskCreate, TaskFullResponse, TaskStatusResponse, TaskUpdate
from task.models import Priority, Status, Task, TaskAssignee, TaskPriority, TaskStatus
from sqlalchemy import func
from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int) -> Task | None:
        task = self.db.query(Task).filter(Task.task_id == task_id).first()
        return task
    
    # def get_last_assignee(self, tasks: List[Task]) -> List[TaskAssigneeResponse]:   
    #     for task in tasks:
    #         # последний исполнитель
    #         last_assignee_row = (
    #             self.db.query(TaskAssignee.assignee_id, User.login, TaskAssignee.assignee_dt)
    #             .join(User, TaskAssignee.assignee_id == User.user_id)
    #             .filter(TaskAssignee.task_id == task.task_id)
    #             .order_by(TaskAssignee.task_assignee_id.desc())
    #             .first()
    #         )

    #         assignee_id, login, assignee_dt = last_assignee_row

    #     return

    # def list(self) -> List[TaskFullResponse]:
    #     tasks = self.db.query(Task).all()
    #     result = []

    #     for task in tasks:
    #         # последний исполнитель
    #         last_assignee_row = (
    #             self.db.query(TaskAssignee.assignee_id, User.login, TaskAssignee.assignee_dt)
    #             .join(User, TaskAssignee.assignee_id == User.user_id)
    #             .filter(TaskAssignee.task_id == task.task_id)
    #             .order_by(TaskAssignee.task_assignee_id.desc())
    #             .first()
    #         )

    #         # последний статус
    #         last_status_row = (
    #             self.db.query(TaskStatus.status_id, Status.status_title, TaskStatus.status_dt)
    #             .join(Status, TaskStatus.status_id == Status.status_id)
    #             .filter(TaskStatus.task_id == task.task_id)
    #             .order_by(TaskStatus.task_status_id.desc())
    #             .first()
    #         )

    #         assignee_id, login, assignee_dt = last_assignee_row
    #         cur_assignee = TaskAssigneeResponse(
    #                 assignee_id=assignee_id,
    #                 assignee_login=login,
    #                 assignee_dt=assignee_dt
    #             )

    #         status_id, status_title, status_dt = last_status_row
    #         current_status = TaskStatusResponse(
    #                 status_id=status_id,
    #                 status_title=status_title,
    #                 status_dt=status_dt
    #             )

    #         result.append(TaskFullResponse(
    #             task_id=task.task_id,
    #             task_title=task.task_title,
    #             description=task.description,
    #             author_id=task.author_id,
    #             cur_assignee=cur_assignee,
    #             current_status=current_status
    #         ))

    #     return result

    def user_created_list(self, user_id: int) -> List[Task]:
        user_tasks = self.db.query(Task).filter(Task.author_id == user_id).all()
        return user_tasks
    
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
    
    # def user_assigned_list(self, assignee_id: int) -> List[TaskFullResponse]:
    #     tasks = self.list()
    
    #     result = []
    #     for task in tasks:
    #         # последний исполнитель
    #         last_assignee = (
    #             self.db.query(TaskAssignee)
    #             # .join(User, TaskAssignee.assignee_id == User.user_id)
    #             .filter(TaskAssignee.task_id == task.task_id)
    #             .order_by(TaskAssignee.task_assignee_id.desc())
    #             .first()
    #         )
    #         # последний статус
    #         last_status_row = (
    #             self.db.query(TaskStatus, Status.status_title)
    #             .join(Status, TaskStatus.status_id == Status.status_id)
    #             .filter(TaskStatus.task_id == task.task_id)
    #             .order_by(TaskStatus.task_status_id.desc())
    #             .first()
    #         )
    #         last_status, status_title = last_status_row if last_status_row else (None, None)
            
    #         result.append(TaskFullResponse(
    #             task_id=task.task_id,
    #             task_title=task.task_title,
    #             description=task.description,
    #             author_id=task.author_id,
    #             cur_assignee=TaskAssigneeResponse.from_orm(last_assignee) if last_assignee else None,
    #             cur_status=TaskStatusResponse.from_orm(status_title)
    #         ))
    #     return result

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
    