"""
==========================================================
AML Investigation Platform

Investigation Request

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.investigation.investigation_scope import (
    InvestigationScope,
)


@dataclass(slots=True)
class InvestigationRequest:
    """
    Complete investigation request.
    """

    case_id: str

    analyst: str

    scope: InvestigationScope