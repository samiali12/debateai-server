from fastapi import APIRouter, Body
from .service import AiModeratorService

router = APIRouter(prefix="/ai-moderator", tags=["AI Moderator"])
ai_moderator_service = AiModeratorService()


@router.post("/analyze-message")
async def analyze_message(message: str = Body(..., embed=True)):
    result = ai_moderator_service.analyze_text(message)
    return {
        "message": "AI moderation result",
        "status_code": 200,
        "data": result,
    }


@router.post("/suggest-question")
async def suggest_question(
    topic: str = Body(...), history: list[str] = Body(default=[])
):
    suggestion = ai_moderator_service.generate_next_question(topic, history)
    return {
        "message": "AI suggested the next question",
        "status_code": 200,
        "data": {"suggestion": suggestion},
    }


@router.post("/fairness-check")
async def fairness_check(
    for_count: int = Body(...),
    against_count: int = Body(...),
):
    analysis = ai_moderator_service.check_fairness(for_count, against_count)
    return {
        "message": "Fairness evaluation",
        "status_code": 200,
        "data": analysis,
    }
