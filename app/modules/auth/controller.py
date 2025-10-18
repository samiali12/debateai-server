from fastapi import APIRouter, Depends
from modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from modules.auth.service import AuthService
from core.middleware import is_authenticated, get_refresh_token
from datetime import datetime, UTC
from database.redis import redis_client
from core.response import ApiResponse

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

@router.get("/refresh-token")
async def refresh_token(
    user: dict = Depends(get_refresh_token),
    service: AuthService = Depends(get_auth_service),
):
    return service.generate_refresh_token(
        user["id"], user["fullName"], user["email"], user["role"], user["token"]
    )

@router.get("/logout")
async def logout(user: dict = Depends(is_authenticated)):
    exp = user.get("exp")
    token = user.get("token")
    if exp:
        ttl = exp - int(datetime.now(UTC).timestamp())
        if ttl < 0:
            ttl = 0
        else:
            ttl = 900
    redis_client.setex(f"blacklist:{token}", ttl, "revoked")
    return ApiResponse(message=f"User {user['email']} logged out successfully.")


@router.get("/me")
async def me(
    user: dict = Depends(is_authenticated),
    service: AuthService = Depends(get_auth_service),
):
    return service.me(user["email"])


@router.put("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    user: dict = Depends(is_authenticated),
    service: AuthService = Depends(get_auth_service),
):
    return service.changed_password(
        user["email"], request.old_password, request.new_password
    )


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    print(request)
    return service.forget_password(request.email)

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.reset_password(request.token, request.newPassword)

