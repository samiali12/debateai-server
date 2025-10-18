from fastapi import HTTPException, status
from core.security import verify_token
from database.redis import redis_client
from fastapi import Request


def is_authenticated(request: Request):
    token = request.cookies.get("access_token")
    if redis_client.get(f"blacklist:{token}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked"
        )

    if not isinstance(token, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    payload.update({"token": token})
    return payload


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not isinstance(token, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    payload.update({"token": token})
    return payload
