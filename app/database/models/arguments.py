from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Float, Enum
from sqlalchemy.sql import func
from database.session import base
import enum


class ArgumentRole(enum.Enum):
    for_side = "for"
    against_side = "against"
    neutral = "neutral"


class Arguments(base):
    __tablename__ = "arguments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(Enum(ArgumentRole), nullable=False)
    content = Column(Text, nullable=False)
    ai_score = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
