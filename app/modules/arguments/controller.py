from fastapi import APIRouter, Depends
from core.middleware import is_authenticated, get_refresh_token
from modules.arguments.service import ArgumentService

router = APIRouter(prefix="/arguments", tags=["Auth"])

argument_service = ArgumentService()

@router.get("/{debate_id}")
async def get_arguments(debate_id: int):
    return argument_service.get_arguments(debate_id)
