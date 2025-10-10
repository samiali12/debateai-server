from fastapi import APIRouter, Depends
from modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
)
from modules.auth.service import AuthService
from core.middleware import is_authenticated

from fastapi import Request


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service():
    return AuthService()


@router.post("/register")
async def register_user(
    request: RegisterRequest, service: AuthService = Depends(get_auth_service)
):
    return service.register(request)


@router.post("/login")
async def login_user(
    request: LoginRequest, service: AuthService = Depends(get_auth_service)
):
    return service.login(request.email, request.password)


@router.get("/me")
async def me(
    user: dict = Depends(is_authenticated),
    service: AuthService = Depends(get_auth_service),
):
    return service.me(user["email"])
