from database.connection import create_tables, wait_for_db
from task.routes import router as task_router
from user.routes import router as user_router
from stats.routes import router as stats_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='Сервис управления задачами')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Старт сервиса управления задачами')
    try:
        wait_for_db(max_attempts=5, wait_seconds=3)
        logger.info('Подключение к БД успешно')
    except Exception as e:
        logger.error(f"БД не готова: {e}")
    yield
    logger.info('Сервис остановлен')


@app.on_event("startup")
def startup_event():
    # create_tables()
    ...

@app.get("/")
def root():
    logger.info('Работа сервиса управления задачами')

app.include_router(task_router)
app.include_router(user_router)
app.include_router(stats_router)
