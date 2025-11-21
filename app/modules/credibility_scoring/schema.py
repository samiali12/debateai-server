from pydantic import BaseModel
from typing import Optional


class ArgumentInput(BaseModel):
    argument_id: int
    participant_id: int
    debate_id: int
    text: str


class ScoreOutput(BaseModel):
    argument_id: int
    participant_id: int
    relevance_score: float
    evidence_score: float
    consistency_score: float
    overall_strength: float
    notes: Optional[str] = None
