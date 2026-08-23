"""
==========================================================
AML Investigation Platform

Authentication Controller

Responsibilities
----------------
✓ Accept API DTOs
✓ Convert DTOs to Domain Models
✓ Invoke Authentication Service
✓ Return Response DTOs

==========================================================
"""

from __future__ import annotations

from app.api.auth.schemas.login_request_dto import LoginRequestDTO
from app.api.auth.schemas.login_response_dto import LoginResponseDTO

from app.api.auth.schemas.register_request_dto import RegisterRequestDTO
from app.api.auth.schemas.register_response_dto import RegisterResponseDTO

from app.services.auth.factories.authentication_factory import (
    AuthenticationFactory,
)

from app.services.auth.services.authentication_service import (
    AuthenticationService,
)


class AuthenticationController:

    def __init__(
        self,
        authentication_service: AuthenticationService,
    ) -> None:

        self._authentication_service = authentication_service

    # =====================================================
    # Register
    # =====================================================

    def register(
        self,
        request: RegisterRequestDTO,
    ) -> RegisterResponseDTO:

        domain_request = (
            AuthenticationFactory.to_register_request(
                request
            )
        )

        return self._authentication_service.register(
            domain_request
        )

    # =====================================================
    # Login
    # =====================================================

    def login(
        self,
        request: LoginRequestDTO,
    ) -> LoginResponseDTO:

        domain_request = (
            AuthenticationFactory.to_login_request(
                request
            )
        )

        return self._authentication_service.login(
            domain_request
        )