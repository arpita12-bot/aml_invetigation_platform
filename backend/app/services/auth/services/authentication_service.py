"""
==========================================================
AML Investigation Platform

Authentication Service

Responsibilities
----------------
✓ Register User
✓ Authenticate User
✓ Generate JWT
==========================================================
"""

from __future__ import annotations

from app.api.auth.schemas.login_response_dto import (
    LoginResponseDTO,
    UserResponseDTO,
)
from app.api.auth.schemas.register_response_dto import (
    RegisterResponseDTO,
)

from app.services.auth.models.login_request import LoginRequest
from app.services.auth.models.register_request import RegisterRequest

from app.services.auth.repositories.authentication_repository import (
    AuthenticationRepository,
)

from app.services.auth.security.password_service import (
    PasswordService,
)

from app.services.auth.security.jwt_service import (
    JwtService,
)


class AuthenticationService:

    def __init__(
        self,
        repository: AuthenticationRepository,
        password_service: PasswordService,
        jwt_service: JwtService,
    ):

        self._repository = repository
        self._password_service = password_service
        self._jwt_service = jwt_service

    # --------------------------------------------------

    def register(
        self,
        request: RegisterRequest,
    ) -> RegisterResponseDTO:

        if self._repository.username_exists(
            request.username,
        ):
            raise ValueError(
                "Username already exists."
            )

        if self._repository.email_exists(
            request.email,
        ):
            raise ValueError(
                "Email already exists."
            )

        hashed_password = self._password_service.hash_password(
            request.password
        )

        self._repository.register_user(

            username=request.username,

            email=request.email,

            hashed_password=hashed_password,

            first_name=request.first_name,

            last_name=request.last_name,

        )

        return RegisterResponseDTO(

            success=True,

            message="User registered successfully.",

        )

    # --------------------------------------------------

    def login(
        self,
        request: LoginRequest,
    ) -> LoginResponseDTO:

        user = self._repository.find_by_username(
            request.username
        )

        if user is None:
            raise ValueError(
                "Invalid username or password."
            )

        if not self._password_service.verify_password(
            request.password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid username or password."
            )

        token = self._jwt_service.create_access_token(

            user_id=user.id,

            username=user.username,

            role=user.role,

        )

        return LoginResponseDTO(

            access_token=token,

            user=UserResponseDTO(

                id=user.id,

                username=user.username,

                email=user.email,

                role=user.role,

            ),

        )