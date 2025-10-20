from pydantic import BaseModel
from typing import Dict

class SummaryResponse(BaseModel):
    debate_id: int
    summary: Dict[str, str]