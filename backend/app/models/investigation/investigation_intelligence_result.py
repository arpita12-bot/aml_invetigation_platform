"""
==========================================================
AML Investigation Platform

Investigation Intelligence Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.risk.risk_score import RiskScore


@dataclass(slots=True)
class InvestigationIntelligenceResult:
    """
    Final intelligence produced for an investigation.
    """

    risk_score: RiskScore

    explanations: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    execution_time_seconds: float = 0.0

    successful: bool = False

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)