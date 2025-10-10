from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Any


class ApiResponse(BaseModel):
    message: str
    status_code: int = 200
    data: Optional[Any] = None


def success_response(message: str, data=None, status_code: int = 200):
    return JSONResponse(
        content={"success": True, "message": message, "data": data},
        status_code=status_code,
    )


def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        content={"success": False, "message": message}, status_code=status_code
    )
