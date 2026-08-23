"""
==========================================================
AML Investigation Platform

User Repository

Responsibilities
----------------
✓ User CRUD operations
✓ User lookup
✓ Authentication queries
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_profile import UserProfile


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------
    # Get user by username
    # -----------------------------------------
    def get_by_username(self, username: str):

        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    # -----------------------------------------
    # Get user by email
    # -----------------------------------------
    def get_by_email(self, email: str):

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    # -----------------------------------------
    # Get user by id
    # -----------------------------------------
    def get_by_id(self, user_id: int):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # -----------------------------------------
    # Create User
    # -----------------------------------------
    def create_user(self, user: User):

        self.db.add(user)
        self.db.flush()

        return user

    # -----------------------------------------
    # Create Profile
    # -----------------------------------------
    def create_profile(self, profile: UserProfile):

        self.db.add(profile)
        self.db.flush()

        return profile

    # -----------------------------------------
    # Commit Transaction
    # -----------------------------------------
    def commit(self):

        self.db.commit()

    # -----------------------------------------
    # Rollback
    # -----------------------------------------
    def rollback(self):

        self.db.rollback()

    # -----------------------------------------
    # Refresh Entity
    # -----------------------------------------
    def refresh(self, entity):

        self.db.refresh(entity)