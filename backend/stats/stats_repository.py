from stats.schemas import ProductiveUsersResponse, StatusAvgTimeResponse
from task.models import Task, TaskStatus, Status
from typing import Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import text


class StatsRepository:
    def __init__(self, db: Session):
        self.db = db

    # получаем сколько задачи пребывают в каждом статусе в миллисекундах в среднем
    def get_task_status_avg_time(self) -> List[StatusAvgTimeResponse]:
        query = '''
            select 
                s.status_title as status_title,
                avg(intervals.duration_sec) as avg_duration_sec
            from (
                select 
                    ts.status_id,
                    timestampdiff(second, ts.status_dt, lead(ts.status_dt) 
                    over (partition by ts.task_id order by ts.status_dt)) as duration_sec
                from task_status ts
            ) as intervals
            join statuses s on intervals.status_id = s.status_id
            where intervals.duration_sec is not null
            group by s.status_id, s.status_title;

        '''
        rows = self.db.execute(text(query)).fetchall()
        result = [
                    {
                        "status_title": row.status_title,
                        "avg_duration_sec": round(row.avg_duration_sec, 2)
                    }
                    for row in rows
                ]
        return result
    
    def get_top_productive_users(self, limit: int = 3) -> List[ProductiveUsersResponse]:  
        query = f'''
            select 
            users.login as assignee_login, 
            count(*) as completed_tasks
            from users join task_assignee on users.user_id = task_assignee.assignee_id
            group by users.login
            limit {limit}
        '''
        rows = self.db.execute(text(query)).fetchall()
        result = [
                    {
                        "login": row.assignee_login,
                        "completion_time_sec": row.completed_tasks
                    }
                    for row in rows
                ]
        return result