from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    return service.register(request)


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    return service.login(request)