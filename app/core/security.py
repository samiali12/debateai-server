import jwt
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from argon2 import PasswordHasher
from datetime import datetime, timedelta, UTC

load_dotenv()

def password_hashing(raw: str):
    ph = PasswordHasher()
    hash = ph.hash(raw)
    return hash


def verify_password(hash: str, password: str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hash, password)
        return True
    except Exception as e:
        return False


def generate_token(
    id: int,
    fullName: str,
    email: str,
    role: str,
    expires_delta: timedelta | None = None,
):
    to_encode = {
        "id": id,
        "fullName": fullName,
        "email": email,
        "role": role,
        "role": role.value if hasattr(role, "value") else role,
    }
    expire = datetime.now(UTC) + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt

def generate_refresh_token(
    id: int,
    fullName: str,
    email: str,
    role: str,
    expires_delta: timedelta | None = None,
):
    to_encode = {
        "id": id,
        "fullName": fullName,
        "email": email,
        "role": role,
        "role": role.value if hasattr(role, "value") else role,
    }
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt

def verify_token(token: str):
    try:
        decode = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
        return decode
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
