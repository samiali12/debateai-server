import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Enum, ForeignKey
from database.session import base


class DebateStatus(enum.Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class UserRole(enum.Enum):
    for_side = "for_side"
    against_side = "against_side"
    neutral = "neutral"


class Debates(base):
    __tablename__ = "debates"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(DebateStatus), default=DebateStatus.active, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_by": self.created_by,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
