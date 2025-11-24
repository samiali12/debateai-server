from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from database.session import base


class Summaries(base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    download_url = Column(String(200), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
