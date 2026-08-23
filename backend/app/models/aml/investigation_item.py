"""
==========================================================
AML Investigation Platform

Investigation Item

Represents a single investigation result returned
from the AML investigation engine.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.models.aml.risk_score import RiskScore
from app.models.aml.shell_company_assessment import (
    ShellCompanyAssessment,
)
from app.models.aml.investigation_recommendation import (
    InvestigationRecommendation,
)


@dataclass(slots=True)
class InvestigationItem:
    """
    Represents one investigated entity/prediction.
    """

    entity_id: str

    entity_type: str

    risk_score: RiskScore

    shell_company_assessment: ShellCompanyAssessment

    recommendations: list[InvestigationRecommendation] = field(
        default_factory=list
    )

    evidence: list[dict[str, Any]] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict:

        return {

            "entity_id": self.entity_id,

            "entity_type": self.entity_type,

            "risk_score": self.risk_score.to_dict(),

            "shell_company_assessment":
                self.shell_company_assessment.to_dict(),

            "recommendations": [

                recommendation.to_dict()

                for recommendation in self.recommendations

            ],

            "evidence": self.evidence,

            "metadata": self.metadata,

        }