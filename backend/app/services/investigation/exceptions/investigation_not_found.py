"""
==========================================================
AML Investigation Platform

Investigation Not Found Exception

==========================================================
"""

from __future__ import annotations

from app.services.investigation.exceptions.investigation_exception import (
    InvestigationException,
)


class InvestigationNotFoundException(
    InvestigationException
):
    """
    Raised when an investigation cannot
    be located.
    """

    pass