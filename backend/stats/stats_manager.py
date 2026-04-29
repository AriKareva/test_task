from stats.stats_repository import StatsRepository
from stats.schemas import ProductiveUsersFullResponse, StatusAvgTimeResponse, ProductiveUsersResponse, StatusAvgTimeFullResponse
from task.models import Task
from typing import Any, List
from fastapi import HTTPException, status


class StatsManager:
    def __init__(self, rep: StatsRepository):
        self.rep = rep

    def _get_task_status_avg_time(self) -> List[StatusAvgTimeResponse]:
        return self.rep.get_task_status_avg_time()
    
    def get_formated_task_status_avg_time(self) -> List[StatusAvgTimeFullResponse]:
        status_avg_time = self._get_task_status_avg_time()
        return [
                    StatusAvgTimeFullResponse(
                        status_title=item['status_title'],
                        days=int(item['avg_duration_sec'] // 86400),
                        hours=int((item['avg_duration_sec'] % 86400) // 3600),
                        minutes=int((item['avg_duration_sec'] % 3600) // 60),
                        avg_duration_sec=int(item['avg_duration_sec'])
                    )
                    for item in status_avg_time
                ]   
    
    def _get_top_productive_users(self, limit: int = 3) -> List[ProductiveUsersResponse]:
        return self.rep.get_top_productive_users(limit=limit)
    
    def get_formatted_top_productive_users(self, limit: int = 3) -> List[ProductiveUsersFullResponse]:
        top_productive_users = self._get_top_productive_users(limit=limit)
        return [
                    ProductiveUsersFullResponse(
                        login=item['login'],
                        # days=int(item['completion_time_sec'] // 86400),
                        # hours=int((item['completion_time_sec'] % 86400) // 3600),
                        # minutes=int((item['completion_time_sec'] % 3600) // 60),
                        days=int(item['completion_time_sec']),
                        hours=int((item['completion_time_sec'])),
                        minutes=int((item['completion_time_sec'])),
                        completion_time_sec=int(item['completion_time_sec'])
                    )
                    for item in top_productive_users
                ]   