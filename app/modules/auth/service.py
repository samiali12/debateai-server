from modules.auth.repository import AuthRepository
from modules.auth.schemas import RegisterRequest, RegisterResponse, LoginResponse
from core.security import password_hashing, generate_token
from core.response import ApiResponse

class AuthService:
    def __init__(self, repo: AuthRepository = AuthRepository()):
        self.repo = repo 
    
    def register(self, data: RegisterRequest) -> RegisterResponse:
        hash = password_hashing(data.password)
        user = self.repo.create_user(data.fullName, data.email, hash, data.role)
        return RegisterResponse(
            id=user.id,
            fullName=user.fullName,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def login(self, email: str, password: str) -> LoginResponse:
        user = self.repo.login_user(email, password)
        if user:
            access_token = generate_token(user.id, user.fullName, user.email, user.role)
            refresh_token = generate_token(user.id, user.fullName, user.email, user.role)
            data = {
                'id': user.id,
                'fullName': user.fullName,
                'email': user.email,
                'role': user.role,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            return ApiResponse(
                message= 'User login successfully',
                status_code=200,
                data=data
            )
