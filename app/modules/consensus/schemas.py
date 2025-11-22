from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class SideSummary(BaseModel):
    role: str
    summary: str
    top_points: List[str] = []


class RecommendationItem(BaseModel):
    id: Optional[int]
    text: str
    type: str
    confidence: float
    fairness: float
    feasibility: float


class ConsensusResponse(BaseModel):
    debate_id: int
    generated_at: datetime
    for_summary: SideSummary
    against_summary: SideSummary
    shared_goals: List[str]
    top_conflicts: List[str]
    recommendations: List[RecommendationItem]
