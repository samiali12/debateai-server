from pydantic import BaseModel
from datetime import datetime


class ArgumentResponse(BaseModel):
    id: int
    debate_id: int
    user_id: int
    role: str
    content: str
    ai_score: int
    created_at: datetime
