from fastapi import APIRouter, Depends
from modules.summerization.service import SummerizationService
from core.middleware import is_authenticated


router = APIRouter(prefix="/summarization", tags=["Summarization"])

summerizerization_service = SummerizationService()


@router.get("/debates/{debate_id}/summarize")
async def summarize_debate(debate_id: int, user: dict = Depends(is_authenticated)):
    return summerizerization_service.generate_summary(debate_id)
