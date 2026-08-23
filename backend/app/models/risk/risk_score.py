"""
==========================================================
AML Investigation Platform

Risk Score

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.risk.risk_factor import RiskFactor


@dataclass(slots=True)
class RiskScore:

    total_score: float

    level: str

    factors: list[RiskFactor] = field(default_factory=list)