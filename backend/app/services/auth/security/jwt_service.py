"""
==========================================================
AML Investigation Platform

JWT Service

Responsibilities
----------------
✓ Generate JWT Access Token
✓ Verify JWT Token
✓ Decode JWT Claims

==========================================================
"""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from typing import Any

from jose import JWTError
from jose import jwt

from app.core.config import settings


class JwtService:

    def create_access_token(
        self,
        user_id: int,
        username: str,
        role: str,
    ) -> str:
        """
        Generate JWT access token.
        """

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode and validate JWT.
        """

        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    def verify_token(
        self,
        token: str,
    ) -> bool:

        try:

            self.decode_token(token)

            return True

        except JWTError:

            return False