from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base  # или from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    reg_dt: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    task_title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    assignee_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

class Status(Base):
    __tablename__ = "statuses"

    status_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    status_title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

class TaskStatus(Base):
    __tablename__ = "task_status"

    task_status_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    start_dt: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    end_dt: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )

class File(Base):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_dt: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

class TaskFile(Base):
    __tablename__ = "task_file"

    task_file_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    file_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)