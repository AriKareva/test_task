from typing import Any, List, Optional
from dependencies import get_stats_manager
from stats.stats_manager import StatsManager
from stats.schemas import ProductiveUsersFullResponse, StatusAvgTimeFullResponse, ProductiveUsersFullResponse
from fastapi import APIRouter, Depends


router = APIRouter(prefix='/statistics', tags=['statistics'])

@router.get('/status-avg-time', response_model=List[StatusAvgTimeFullResponse])
def get_status_avg_time(
    manager: StatsManager = Depends(get_stats_manager)
):
    return manager.get_formated_task_status_avg_time()
    

@router.get('/top-productive-users', response_model=List[ProductiveUsersFullResponse])
def get_top_productive_users(
    limit: Optional[int] = 3,
    manager: StatsManager = Depends(get_stats_manager)
):
    return manager.get_formatted_top_productive_users(limit=limit)
    