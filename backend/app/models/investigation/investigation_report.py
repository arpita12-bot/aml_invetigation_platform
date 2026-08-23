"""
==========================================================
AML Investigation Platform

Investigation Report

==========================================================
"""

from dataclasses import dataclass, field

from app.models.recommendation import Recommendation
from app.models.shell_candidate import ShellCandidate


@dataclass(slots=True)
class InvestigationReport:

    case_id: str

    entity_id: str

    entity_type: str

    analyst: str

    risk_level: str

    risk_score: float

    summary: str

    shell_candidates: list[ShellCandidate]

    recommendations: list[Recommendation]

    execution_time_seconds: float

    successful: bool

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)