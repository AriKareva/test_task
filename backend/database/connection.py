import time
from sqlite3 import OperationalError
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

def wait_for_db(max_attempts=30, wait_seconds=2):
    for attempt in range(1, max_attempts + 1):
        try:
            db_engine.connect()
            print(f'Подключение к MySQL успешно (попытка {attempt})')
            return
        except OperationalError:
            print(f'MySQL ещё не готов, попытка {attempt}/{max_attempts}...')
            time.sleep(wait_seconds)
    raise Exception('MySQL не стал доступен после ожидания')


def create_tables():
    wait_for_db()
    Base.metadata.create_all(bind=db_engine)
    log.info('Таблцы созданы в БД')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
