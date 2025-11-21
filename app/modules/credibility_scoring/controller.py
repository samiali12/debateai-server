from fastapi import APIRouter
from .service import CredibilityScoringService
from .schema import ArgumentInput, ScoreOutput

router = APIRouter(prefix="/credibility", tags=["Credibility Scoring"])

service = CredibilityScoringService()

@router.post("/score-argument", response_model=ScoreOutput)
def score_argument(request: ArgumentInput):
    return service.score_argument(request)
