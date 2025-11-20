from fastapi import APIRouter
from modules.tone_civility.service import ToneCivilityService
from .schemas import ToneCivilityRequest

router = APIRouter(prefix="/tone-civility", tags=["Tone and Civility"])

tone_civility_service = ToneCivilityService()


@router.post("/analyse")
async def analyse_tone_civility(request: ToneCivilityRequest):
    return tone_civility_service.analyze_tone_civility(request.argument_id, request.text)
