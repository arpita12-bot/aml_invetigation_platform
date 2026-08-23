"""
==========================================================
AML Investigation Platform

Current User Dependency
==========================================================
"""

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.auth.dependencies.bearer import JwtBearer

from app.services.auth.repositories.authentication_repository import (
    AuthenticationRepository,
)

from app.services.auth.security.jwt_service import JwtService


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(JwtBearer),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    jwt_service = JwtService()
    repository = AuthenticationRepository(db)

    try:
        payload = jwt_service.decode_token(token)
        user_id = int(payload["sub"])

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = repository.find_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    return user