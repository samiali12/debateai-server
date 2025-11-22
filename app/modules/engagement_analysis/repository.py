from sqlalchemy.orm import Session
from database.session import session
from database.models.arguments import Arguments
from database.models.participants import Participants
from database.models.users import Users
from sqlalchemy import func


class EngagementRepository:

    def __init__(self):
        self.db = session()

    def get_engagement_over_time(self, debate_id: int):
        return (
            self.db.query(
                func.date_format(Arguments.created_at, "%Y-%m-%d %H:%i:00").label(
                    "timestamp"
                ),
                func.count(Arguments.id).label("count"),
            )
            .filter(Arguments.debate_id == debate_id)
            .group_by(func.date_format(Arguments.created_at, "%Y-%m-%d %H:%i:00"))
            .order_by("timestamp")
            .all()
        )

    def get_user_activity(self, debate_id: int):
        return (
            self.db.query(
                Users.id, Users.fullName, func.count(Arguments.id).label("count")
            )
            .join(Users, Users.id == Arguments.user_id)
            .filter(Arguments.debate_id == debate_id)
            .group_by(Users.id)
            .all()
        )

    def get_role_trends(self, debate_id: int):
        """Get role trends over time using MySQL DATE_FORMAT"""
        return (
            self.db.query(
                func.date_format(Arguments.created_at, "%Y-%m-%d %H:%i:00").label(
                    "timestamp"
                ),
                func.sum(func.if_(Participants.role == "for_side", 1, 0)).label(
                    "for_count"
                ),
                func.sum(func.if_(Participants.role == "against_side", 1, 0)).label(
                    "against_count"
                ),
                func.sum(func.if_(Participants.role == "neutral", 1, 0)).label(
                    "neutral_count"
                ),
            )
            .join(
                Participants,
                (Arguments.user_id == Participants.user_id)
                & (Arguments.debate_id == Participants.debate_id),
            )
            .filter(Arguments.debate_id == debate_id)
            .group_by(func.date_format(Arguments.created_at, "%Y-%m-%d %H:%i:00"))
            .order_by("timestamp")
            .all()
        )
