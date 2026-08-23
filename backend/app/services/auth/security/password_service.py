"""
==========================================================
AML Investigation Platform

Password Service

Responsibilities
----------------
✓ Hash passwords
✓ Verify passwords

==========================================================
"""

from __future__ import annotations

from passlib.context import CryptContext


class PasswordService:

    def __init__(self) -> None:

        self._context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash_password(
        self,
        password: str,
    ) -> str:
        
        print("PASSWORD TYPE :", type(password))
        print("PASSWORD VALUE:", repr(password))
        print("PASSWORD LENGTH:", len(password))

        return self._context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:

        return self._context.verify(
            plain_password,
            hashed_password,
        )