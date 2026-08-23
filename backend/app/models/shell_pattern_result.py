"""
==========================================================
AML Investigation Platform

Shell Pattern Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.shell_candidate import (
    ShellCandidate,
)


@dataclass(slots=True)
class ShellPatternResult:
    """
    Final shell company detection result.
    """

    candidates: list[ShellCandidate]

    execution_time_seconds: float

    successful: bool

    total_candidates: int

    high_risk_candidates: int = 0

    medium_risk_candidates: int = 0

    low_risk_candidates: int = 0

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )