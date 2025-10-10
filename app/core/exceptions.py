from fastapi import HTTPException, status


class DatabaseConnectionError(HTTPException):
    def __init__(self, detail: str = "Database connection failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class UserAlreadyExistsError(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{email}' already exists.",
        )


class InvalidCredentialsError(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message or "Invalid email or password.",
        )


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "An internal server error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
