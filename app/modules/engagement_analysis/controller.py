from fastapi import APIRouter
from .service import EngagementService
from .schemas import DebateTrendsOutput

router = APIRouter(prefix="/engagement", tags=["Engagement Analysis"])

service = EngagementService()


@router.get("/{debate_id}", response_model=DebateTrendsOutput)
def get_debate_trends(debate_id: int):
    return service.get_trends(debate_id)
