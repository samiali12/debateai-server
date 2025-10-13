import os
import jwt
from modules.auth.repository import AuthRepository
from modules.auth.schemas import RegisterRequest, RegisterResponse, LoginResponse
from core.security import password_hashing, generate_token, generate_refresh_token
from core.response import ApiResponse
from tasks.email_tasks import send_reset_password_link
from core.security import verify_token
from database.models.users import UserRole


class AuthService:
    def __init__(self, repo: AuthRepository = AuthRepository()):
        self.repo = repo

    def register(self, data: RegisterRequest) -> RegisterResponse:
        hash = password_hashing(data.password)
        user = self.repo.create_user(data.fullName, data.email, hash, data.role)
        print(f"user.role repr: {repr(user.role)}")
        return RegisterResponse(
            id=user.id,
            fullName=user.fullName,
            email=user.email,
            role=user.role.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def login(self, email: str, password: str) -> LoginResponse:
        user = self.repo.login_user(email, password)
        if user:
            access_token = generate_token(user.id, user.fullName, user.email, user.role)
            refresh_token = generate_refresh_token(
                user.id, user.fullName, user.email, user.role
            )
            data = {
                "id": user.id,
                "fullName": user.fullName,
                "email": user.email,
                "role": user.role,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            return ApiResponse(
                message="User login successfully", status_code=200, data=data
            )

    def me(self, email: str):
        user = self.repo.me(email)
        data = {
            "id": user.id,
            "fullName": user.fullName,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        return ApiResponse(message="User data", status_code=200, data=data)

    def changed_password(self, email: str, old_password: str, new_password: str):
        flag = self.repo.change_password(email, old_password, new_password)
        if flag:
            return ApiResponse(
                message=f"Password changed successfully for user {email}"
            )

    def forget_password(self, email: str):
        flag = self.repo.forget_password(email)
        if flag:
            token = jwt.encode(
                {"email": email}, os.getenv("SECRET_KEY"), algorithm="HS256"
            )
            send_reset_password_link(email, token)
            return ApiResponse(message="Password reset email sent successfully")

    def reset_password(self, token: str, new_password: str):
        decode = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
        flag = self.repo.reset_password(decode["email"], new_password)
        if flag:
            return ApiResponse(message="Password reset successfully")

    def refresh_token(
        self,
        id: int,
        fullName: str,
        email: str,
        role: str,
        refresh_token: str,
    ):
        flag = verify_token(refresh_token)
        if flag:
            access_token = generate_refresh_token(id, fullName, email, role)
            new_refresh_token = generate_refresh_token(id, fullName, email, role)
            return ApiResponse(
                message="successfully re generate access and refresh token",
                data={"access_token": access_token, "refresh_token": new_refresh_token},
            )
