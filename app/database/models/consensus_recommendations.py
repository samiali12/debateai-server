from sqlalchemy import JSON, Column, Integer, String, Text, DateTime, func
from datetime import datetime
from database.session import base


class ConsensusRecommendation(base):
    __tablename__ = "consensus_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, index=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    payload = Column(JSON)
    summary_text = Column(Text)
    generated_by = Column(String(128), default="system")

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
