from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func, Column
from database.connection import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_title = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, nullable=True)
    author_id = Column(BigInteger, nullable=False)
    assignee_id = Column(BigInteger, nullable=False)

class Status(Base):
    __tablename__ = "statuses"

    status_id = Column(BigInteger, primary_key=True, autoincrement=True)
    status_title = Column(String(25), unique=True, nullable=False)

class TaskStatus(Base):
    __tablename__ = "task_status"

    task_status_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, nullable=False)
    status_id = Column(BigInteger, nullable=False)
    start_dt = Column(DateTime, server_default=func.current_timestamp())
    end_dt = Column(DateTime, server_default=func.current_timestamp())

class File(Base):
    __tablename__ = "files"

    file_id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_name = Column(String(255), nullable=False)
    upload_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

class TaskFile(Base):
    __tablename__ = "task_file"

    task_file_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, nullable=False)
    file_id = Column(BigInteger, nullable=True)