from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
from .config import settings


log = logging.getLogger(__name__)
Base = declarative_base()

db_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_pre_ping=settings.POOL_PRE_PING,
)

SessionLocal = sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

def create_tables():
    Base.metadata.create_all(bind=db_engine)
    log.info('Таблцы созданы в БД')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
