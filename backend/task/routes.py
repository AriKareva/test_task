from fastapi import APIRouter


# руты пользователей

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.get('/', response_model=...)
def get_users():
    ...

@user_router.get('/{user_id}', response_model=...)
def get_user():
    ...

@user_router.get('/login', response_model=...)
def login():
    ...

@user_router.post('/register', response_model=...)
def register():
    ...

@user_router.get('/me', response_model=...)
def me():
    ...

@user_router.get('/logout', response_model=...)
def logout():
    ...

# руты задач
task_router = APIRouter(prefix='task', tags=['task'])

@task_router.get('/', response_model=...)
def get_tasks():
    ...

@task_router.get('/{task_id}', response_model=...)
def get_task(task_id: int):
    ...


@task_router.post('/', response_model=...)
def create_task():
    ...

@task_router.delete('/', response_model=...)
def delete_task():
    ...

@task_router.fetch('/', response_model=...)
def update_task():
    ...


# руты статусов
status_router = APIRouter('/status', tags=['status'])


@status_router.get('/', response_model=...)
def get_statuses():
    ...

@status_router.get('/{status_id}', response_model=...)
def get_status(status_id: int):
    ...