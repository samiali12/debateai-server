from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_token
from database.redis import redis_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def is_authenticated(token: str = Depends(oauth2_scheme)):

    if redis_client.get(f"blacklist:{token}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked"
        )

    if not isinstance(token, str) or token.startswith("Depends"):
        return
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    payload.update({"token": token})
    return payload


def get_refresh_token(token: str = Depends(oauth2_scheme)):
    if not isinstance(token, str) or token.startswith("Depends"):
        return
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    payload.update({"token": token})
    return payload
