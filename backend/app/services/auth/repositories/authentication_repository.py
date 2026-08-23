"""
==========================================================
AML Investigation Platform

Authentication Repository

Responsibilities
----------------
✓ User CRUD Operations
✓ User Profile CRUD Operations
✓ User Lookup
✓ Duplicate Validation
✓ Database Persistence

==========================================================
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_profile import UserProfile


class AuthenticationRepository:

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._db = db

    # =====================================================
    # User Lookup
    # =====================================================

    def find_by_username(
        self,
        username: str,
    ) -> Optional[User]:

        return (
            self._db.query(User)
            .filter(User.username == username)
            .first()
        )

    def find_by_email(
        self,
        email: str,
    ) -> Optional[User]:

        return (
            self._db.query(User)
            .filter(User.email == email)
            .first()
        )

    def find_by_id(
        self,
        user_id: int,
    ) -> Optional[User]:

        return (
            self._db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # =====================================================
    # Validation
    # =====================================================

    def username_exists(
        self,
        username: str,
    ) -> bool:

        return self.find_by_username(username) is not None

    def email_exists(
        self,
        email: str,
    ) -> bool:

        return self.find_by_email(email) is not None

    # =====================================================
    # User Creation
    # =====================================================

    def create_user(
        self,
        username: str,
        email: str,
        hashed_password: str,
        role: str = "ANALYST",
    ) -> User:

        user = User(

            username=username,

            email=email,

            hashed_password=hashed_password,

            role=role,

            is_active=True,

        )

        self._db.add(user)

        self._db.flush()

        return user

    # =====================================================
    # User Profile
    # =====================================================

    def create_profile(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
    ) -> UserProfile:

        profile = UserProfile(

            user_id=user_id,

            first_name=first_name,

            last_name=last_name,

        )

        self._db.add(profile)

        return profile

    # =====================================================
    # Transaction Management
    # =====================================================

    def commit(self) -> None:

        self._db.commit()

    def rollback(self) -> None:

        self._db.rollback()

    def refresh(
        self,
        entity,
    ) -> None:

        self._db.refresh(entity)

    # =====================================================
    # Registration
    # =====================================================

    def register_user(
        self,
        username: str,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        role: str = "ANALYST",
    ) -> User:

        try:

            user = self.create_user(

                username=username,

                email=email,

                hashed_password=hashed_password,

                role=role,

            )

            self.create_profile(

                user_id=user.id,

                first_name=first_name,

                last_name=last_name,

            )

            self.commit()

            self.refresh(user)

            return user

        except SQLAlchemyError:

            self.rollback()

            raise