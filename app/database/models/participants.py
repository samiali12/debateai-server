from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from database.session import base
import enum


class Stance(enum.Enum):
    for_side = "for"
    against_side = "against"
    neutral = "neutral"


class Participants(base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    stance = Column(Enum(Stance), nullable=False)
    joined_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
