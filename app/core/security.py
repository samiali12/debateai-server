import jwt
import os
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
