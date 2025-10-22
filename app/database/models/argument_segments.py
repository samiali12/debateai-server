from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey, DateTime, func
from database.session import base 

class ArgumentSegments(base):
    __tablename__ = "argument_segments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    argument_id = Column(Integer, ForeignKey("arguments.id", ondelete="CASCADE"))
    segment_text = Column(Text, nullable=False)
    segment_type = Column(String(50), nullable=True)
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