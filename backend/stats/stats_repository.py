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
                    u.login as assignee_login,
                    avg(timestampdiff(second, tc.first_created_dt, first_done.first_done_dt)) as completion_time_sec
                from (
                    select task_id, min(status_dt) as first_created_dt
                    from task_status
                    where status_id = (select status_id from statuses where status_title = 'создана')
                    group by task_id
                ) tc
                join (
                    select task_id, min(status_dt) as first_done_dt
                    from task_status
                    where status_id = (select status_id from statuses where status_title = 'выполнена')
                    group by task_id
                ) first_done on tc.task_id = first_done.task_id
                join (
                    select ta.task_id, ta.assignee_id
                    from task_assignee ta
                    inner join (
                        select task_id, max(assignee_dt) as max_dt
                        from task_assignee
                        where assignee_dt <= (
                            select min(status_dt) from task_status ts2
                            where ts2.task_id = task_assignee.task_id
                            and ts2.status_id = (select status_id from statuses where status_title = 'выполнена')
                        )
                        group by task_id
                    ) last_ass on ta.task_id = last_ass.task_id and ta.assignee_dt = last_ass.max_dt
                ) last_assignee on tc.task_id = last_assignee.task_id
                join users u on last_assignee.assignee_id = u.user_id
                group by u.user_id, u.login
                order by completion_time_sec asc
                limit {limit}
        '''
        rows = self.db.execute(text(query)).fetchall()
        result = [
                    {
                        "login": row.assignee_login,
                        "completion_time_sec": row.completion_time_sec
                    }
                    for row in rows
                ]
        return result