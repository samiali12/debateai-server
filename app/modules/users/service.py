from fastapi import HTTPException, status
from modules.users.repository import UserRepository
from modules.users.schemas import UpdateProfileRequest

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def update_profile(self, email: str, request: UpdateProfileRequest):
        user = self.repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        update_data = request.model_dump(exclude_unset=True)
        # If email is being updated, check if it already exists
        if "email" in update_data and update_data["email"] != email:
            existing_user = self.repo.get_user_by_email(update_data["email"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        updated_user = self.repo.update_user(user, update_data)
        return {
            "message": "Profile updated successfully",
            "user": {
                "id": updated_user.id,
                "fullName": updated_user.fullName,
                "email": updated_user.email,
                "role": updated_user.role,
            },
        }
