from database.session import base
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class ArgumentScores(base):
    __tablename__ = "argument_scores"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    argument_id = Column(Integer, ForeignKey("arguments.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)

    relevance_score = Column(Float, nullable=False)
    evidence_score = Column(Float, nullable=False)
    consistency_score = Column(Float, nullable=False)
    overall_strength = Column(Float, nullable=False)

    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    argument = relationship("Arguments", back_populates="score")
    participant = relationship("Participants")
