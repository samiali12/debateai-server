from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Float, Enum
from sqlalchemy.sql import func
from database.session import base
from database.models.enums import DebateRole
from sqlalchemy.orm import relationship


class Arguments(base):
    __tablename__ = "arguments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    debate_id = Column(
        Integer, ForeignKey("debates.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(Enum(DebateRole), nullable=False)
    content = Column(Text, nullable=False)
    ai_score = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    civility = relationship(
        "ArgumentCivilityAnalysis",
        back_populates="argument",
        uselist=False,
        cascade="all, delete-orphan",
    )

    score = relationship("ArgumentScores", uselist=False, back_populates="argument")
