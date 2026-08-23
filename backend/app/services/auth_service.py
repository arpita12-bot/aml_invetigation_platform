"""
==========================================================
AML Investigation Platform

Authentication Service
==========================================================
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_profile import UserProfile

from app.repositories.user_repository import UserRepository

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    def __init__(self, db: Session):

        self.repository = UserRepository(db)

    # ------------------------------------------------

    def register(
        self,
        request: RegisterRequest
    ):

        if self.repository.get_by_username(request.username):

            raise HTTPException(
                status_code=400,
                detail="Username already exists."
            )

        if self.repository.get_by_email(request.email):

            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

        user = User(

            username=request.username,
            email=request.email,
            hashed_password=hash_password(
                request.password
            ),

            role="ANALYST",
            status="ACTIVE",
        )

        self.repository.create_user(user)

        profile = UserProfile(

            user_id=user.id,

            first_name=request.first_name,

            last_name=request.last_name
        )

        self.repository.create_profile(profile)

        self.repository.commit()

        self.repository.refresh(user)

        return {

            "message": "User registered successfully."
        }

    # ------------------------------------------------

    def login(
        self,
        request: LoginRequest
    ):

        user = self.repository.get_by_username(
            request.username
        )

        if user is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        if not verify_password(
            request.password,
            user.hashed_password
        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        token = create_access_token(

            {
                "sub": user.username,
                "user_id": user.id,
                "role": user.role,
            }
        )

        return {

            "access_token": token,

            "token_type": "bearer",

            "user": {

                "id": user.id,

                "username": user.username,

                "email": user.email,

                "role": user.role,
            },
        }