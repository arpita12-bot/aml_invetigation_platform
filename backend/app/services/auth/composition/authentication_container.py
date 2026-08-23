"""
==========================================================
AML Investigation Platform

Authentication Composition Container

Responsibilities
----------------
✓ Wire Authentication Dependencies
✓ Build Repository
✓ Build Security Services
✓ Build Authentication Service
✓ Build Controller

==========================================================
"""

from sqlalchemy.orm import Session

from app.api.auth.controller import AuthenticationController

from app.services.auth.repositories.authentication_repository import (
    AuthenticationRepository,
)

from app.services.auth.security.password_service import (
    PasswordService,
)

from app.services.auth.security.jwt_service import (
    JwtService,
)

from app.services.auth.services.authentication_service import (
    AuthenticationService,
)


class AuthenticationContainer:

    def __init__(
        self,
        db: Session,
    ):

        repository = AuthenticationRepository(db)

        password_service = PasswordService()

        jwt_service = JwtService()

        authentication_service = AuthenticationService(
            repository=repository,
            password_service=password_service,
            jwt_service=jwt_service,
        )

        self.controller = AuthenticationController(
            authentication_service
        )