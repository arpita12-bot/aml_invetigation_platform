"""
==========================================================
AML Investigation Platform

Authentication Router

Responsibilities
----------------
✓ Register User
✓ Login User

==========================================================
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.api.auth.schemas.login_request_dto import LoginRequestDTO
from app.api.auth.schemas.login_response_dto import LoginResponseDTO

from app.api.auth.schemas.register_request_dto import RegisterRequestDTO
from app.api.auth.schemas.register_response_dto import RegisterResponseDTO

from app.services.auth.composition.authentication_container import (
    AuthenticationContainer,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponseDTO,
    summary="Register User",
)
def register(
    request: RegisterRequestDTO,
    db: Session = Depends(get_db),
) -> RegisterResponseDTO:

    container = AuthenticationContainer(db)

    return container.controller.register(request)


@router.post(
    "/login",
    response_model=LoginResponseDTO,
    summary="Login User",
)
def login(
    request: LoginRequestDTO,
    db: Session = Depends(get_db),
) -> LoginResponseDTO:

    container = AuthenticationContainer(db)

    return container.controller.login(request)