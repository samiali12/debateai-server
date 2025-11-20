from database.session import base
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship


class ArgumentCivilityAnalysis(base):
    __tablename__ = "argument_civility_analysis"

    id = Column(Integer, primary_key=True, index=True)
    argument_id = Column(Integer, ForeignKey("arguments.id"), nullable=False)
    toxicity_score = Column(Float, nullable=False)
    civility_score = Column(Float, nullable=False)
    flags = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    argument = relationship("Arguments", back_populates="civility")
