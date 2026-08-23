"""
==========================================================
AML Investigation Platform

Authorization Dependency

Responsibilities
----------------
✓ Role Based Authorization

==========================================================
"""

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.auth.dependencies.current_user import (
    get_current_user,
)


def require_roles(*roles):

    def dependency(

        current_user=Depends(get_current_user),

    ):

        if current_user.role not in roles:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Permission denied",

            )

        return current_user

    return dependency