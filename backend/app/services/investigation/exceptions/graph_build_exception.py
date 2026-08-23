"""
==========================================================
AML Investigation Platform

Graph Build Exception

==========================================================
"""

from __future__ import annotations

from app.services.investigation.exceptions.investigation_exception import (
    InvestigationException,
)


class GraphBuildException(
    InvestigationException
):
    """
    Raised when investigation graph
    construction fails.
    """

    pass