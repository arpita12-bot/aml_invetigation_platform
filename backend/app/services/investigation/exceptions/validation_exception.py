"""
==========================================================
AML Investigation Platform

Investigation Validation Exception

==========================================================
"""

from __future__ import annotations

from app.services.investigation.exceptions.investigation_exception import (
    InvestigationException,
)


class InvestigationValidationException(
    InvestigationException
):
    """
    Raised when an investigation request
    fails validation.
    """

    pass