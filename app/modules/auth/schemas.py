import enum
from pydantic import BaseModel, EmailStr, constr, Field
from datetime import datetime

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class RegisterRequest(BaseModel):
    fullName: constr(strip_whitespace=True, min_length=3)  # type: ignore
    email: EmailStr
    password: constr(min_length=8)  # type: ignore

class RegisterResponse(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    role: str
    access_token: str
    refresh_token: str
    created_at: datetime
    updated_at: datetime

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    newPassword: str
    token: str