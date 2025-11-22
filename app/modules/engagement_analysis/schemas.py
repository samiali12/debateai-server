from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    count: int


class UserActivity(BaseModel):
    user_id: int
    name: str
    count: int


class RoleTrend(BaseModel):
    timestamp: datetime
    for_count: int
    against_count: int
    neutral_count: int


class DebateTrendsOutput(BaseModel):
    engagement_over_time: List[TimeSeriesPoint]
    user_activity: List[UserActivity]
    role_trend: List[RoleTrend]
