"""
==========================================================
AML Investigation Platform

Investigation Response

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.investigation.investigation_report import (
    InvestigationReport,
)

from app.models.risk.risk_scoring_result import (
    RiskScoringResult,
)


@dataclass(slots=True)
class InvestigationResponse:

    case_id: str

    status: str

    risk_result: RiskScoringResult

    evidence: list = field(default_factory=list)

    recommendations: list = field(default_factory=list)

    report: InvestigationReport | None = None