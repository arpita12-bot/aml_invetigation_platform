"""
==========================================================
AML Investigation Platform

Authentication Factory

Responsibilities
----------------
✓ Convert RegisterRequestDTO -> RegisterRequest
✓ Convert LoginRequestDTO -> LoginRequest

==========================================================
"""

from app.api.auth.schemas.register_request_dto import RegisterRequestDTO
from app.api.auth.schemas.login_request_dto import LoginRequestDTO

from app.services.auth.models.register_request import RegisterRequest
from app.services.auth.models.login_request import LoginRequest


class AuthenticationFactory:

    @staticmethod
    def to_register_request(
        dto: RegisterRequestDTO,
    ) -> RegisterRequest:

        return RegisterRequest(
            username=dto.username,
            email=dto.email,
            password=dto.password,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )

    @staticmethod
    def to_login_request(
        dto: LoginRequestDTO,
    ) -> LoginRequest:

        return LoginRequest(
            username=dto.username,
            password=dto.password,
        )