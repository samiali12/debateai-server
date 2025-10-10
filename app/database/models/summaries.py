from sqlalchemy import Column, Integer, ForeignKey, Text, String, DateTime
from sqlalchemy.sql import func
from database.session import base


class Summaries(base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    summary_text = Column(Text, nullable=False)
    generated_by = Column(String(50), default="AI Engine", nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
