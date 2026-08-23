"""
==========================================================
AML Investigation Platform

Security Utilities

Responsibilities
----------------
✓ Password hashing
✓ Password verification
✓ JWT generation
==========================================================
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash plain password
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify password
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict) -> str:
    """
    Generate JWT access token
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = data.copy()
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )