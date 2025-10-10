import enum
from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from database.session import base


class UserRole(enum.Enum):
    admin = "admin"
    for_side = "for"
    against_side = "against"
    neutral = "neutral"


class Users(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fullName = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.neutral, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
