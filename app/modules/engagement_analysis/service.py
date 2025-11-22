from .repository import EngagementRepository
from .schemas import DebateTrendsOutput, TimeSeriesPoint, UserActivity, RoleTrend


class EngagementService:

    def __init__(self):
        self.repo = EngagementRepository()

    def get_trends(self, debate_id: int):
        engagement = self.repo.get_engagement_over_time(debate_id)
        activity = self.repo.get_user_activity(debate_id)
        role_trends = self.repo.get_role_trends(debate_id)

        return DebateTrendsOutput(
            engagement_over_time=[
                TimeSeriesPoint(timestamp=row.timestamp, count=row.count)
                for row in engagement
            ],
            user_activity=[
                UserActivity(user_id=row.id, name=row.fullName, count=row.count)
                for row in activity
            ],
            role_trend=[
                RoleTrend(
                    timestamp=row.timestamp,
                    for_count=row.for_count,
                    against_count=row.against_count,
                    neutral_count=row.neutral_count,
                )
                for row in role_trends
            ]
        )
