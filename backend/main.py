from database.connection import create_tables
from task.routes import router as task_router
from user.routes import router as user_router
from stats.routes import router as stats_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='Сервис управления задачами')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def root():
    ...

app.include_router(task_router)
app.include_router(user_router)
app.include_router(stats_router)
