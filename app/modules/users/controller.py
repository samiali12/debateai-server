from fastapi import APIRouter, Depends
from modules.users.service import UserService
from modules.users.schemas import UpdateProfileRequest
from core.middleware import is_authenticated

router = APIRouter(prefix="/users", tags=["Users"])

user_service = UserService()

@router.put("/profile")
async def update_profile(
    request: UpdateProfileRequest,
    user: dict = Depends(is_authenticated),
):
    return user_service.update_profile(user["email"], request)
