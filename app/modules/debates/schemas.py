from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class DebateCreate(BaseModel):
    title: str
    description: str
    role: str


class DebateUpdateStatus(BaseModel):
    status: str


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
    debate_id: int 
    user_id: int 
    role: str 
    content: str 
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
