from sqlalchemy import Column, Integer, ForeignKey, Float, Text, String, DateTime
from sqlalchemy.sql import func
from database.session import base


class Analysis(base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    for_score = Column(Float, nullable=True)
    against_score = Column(Float, nullable=True)
    neutral_score = Column(Float, nullable=True)
    sentiment_summary = Column(Text, nullable=True)
    predicted_winner = Column(String(50), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
