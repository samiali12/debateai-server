from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class DebateCreate(BaseModel):
    title: str
    description: Optional[str] = None


class DebateResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_by: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WSMessage(BaseModel):
    type: str
    user: Optional[str] = None
    role: Optional[str] = None
    content: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
