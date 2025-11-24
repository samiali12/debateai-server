from pydantic import BaseModel, EmailStr
from typing import Optional


class UpdateProfileRequest(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
