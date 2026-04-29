from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func, Column, ForeignKey
from database.connection import Base
from sqlalchemy.orm import relationship


class Priority(Base):
    __tablename__ = 'priorities'

    priority_id = Column(BigInteger, primary_key=True, autoincrement=True)
    priority_title = Column(String(25), unique=True, nullable=False)

    task_priorities = relationship('TaskPriority', back_populates='priority')


class Status(Base):
    __tablename__ = 'statuses'

    status_id = Column(BigInteger, primary_key=True, autoincrement=True)
    status_title = Column(String(25), unique=True, nullable=False)

    task_statuses = relationship('TaskStatus', back_populates='status')


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    deadline =  Column(DateTime, nullable=True)
    author_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    author = relationship('User', foreign_keys=[author_id], back_populates='authored_tasks')
    assignee_history = relationship("TaskAssignee", back_populates="task", cascade="all, delete-orphan", passive_deletes=True)
    priority_history = relationship('TaskPriority', back_populates='task', cascade="all, delete-orphan", passive_deletes=True)
    status_history = relationship('TaskStatus', back_populates='task', cascade="all, delete-orphan", passive_deletes=True)
    # files = relationship('TaskFile', back_populates='task')


class TaskAssignee(Base):
    __tablename__ = 'task_assignee'

    task_assignee_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='SET NULL', onupdate='SET NULL'), nullable=True)
    assignee_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    task = relationship('Task', back_populates='assignee_history')
    assignee = relationship('User', back_populates='assignee_history')


class TaskPriority(Base):
    __tablename__ = 'task_priority'

    task_priority_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey('tasks.task_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    priority_id = Column(BigInteger, ForeignKey('priorities.priority_id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=True)
    priority_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    task = relationship('Task', back_populates='priority_history')
    priority = relationship('Priority', back_populates='task_priorities')


class TaskStatus(Base):
    __tablename__ = 'task_status'

    task_status_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey('tasks.task_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    status_id = Column(BigInteger, ForeignKey('statuses.status_id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    status_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    task = relationship('Task', back_populates='status_history')
    status = relationship('Status', back_populates='task_statuses')


# class TaskFile(Base):
#     __tablename__ = 'task_file'

#     task_file_id = Column(BigInteger, primary_key=True, autoincrement=True)
#     task_id = Column(BigInteger, ForeignKey('tasks.task_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
#     file_name = Column(String(255), nullable=False)
#     upload_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

#     task = relationship('Task', back_populates='files')