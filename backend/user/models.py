from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, DateTime, func, Column
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    reg_dt = Column(DateTime, nullable=False, server_default=func.current_timestamp())

