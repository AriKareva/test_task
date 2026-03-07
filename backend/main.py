from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return pymysql.connect(
        host='db',
        user='root',
        password='password',
        database='test_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/tasks")
def get_tasks(search: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks"
    if search:
        query += f" WHERE title LIKE '%{search}%'"
    
    cursor.execute(query)
    tasks = cursor.fetchall()

    for task in tasks:
        cursor.execute(f"SELECT name FROM users WHERE id = {task['user_id']}")
        user = cursor.fetchone()
        task['user_name'] = user['name'] if user else "Unknown"
    
    conn.close()
    return tasks

@app.post("/tasks")
async def create_task(request: Request):
    data = await request.json()
    title = data.get("title")
    user_id = data.get("user_id", 1)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO tasks (title, user_id) VALUES ('{title}', {user_id})")
    conn.commit()
    conn.close()
    return {"status": "created"}