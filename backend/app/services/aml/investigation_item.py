"""
==========================================================
AML Investigation Platform

Investigation Item

Represents AML intelligence for a single predicted
relationship.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.aml.investigation_recommendation import (
    InvestigationRecommendation,
)
from app.services.aml.risk_scoring.relationship_explanation import (
    RelationshipExplanation,
)
from app.models.aml.risk_score import (
    RiskScore,
)
from app.models.aml.shell_company_assessment import (
    ShellCompanyAssessment,
)
from app.models.prediction.prediction_candidate import (
    PredictionCandidate,
)


@dataclass(slots=True)
class InvestigationItem:

    prediction: PredictionCandidate

    risk: RiskScore

    shell: ShellCompanyAssessment

    explanation: RelationshipExplanation

    recommendation: InvestigationRecommendation

    def to_dict(self) -> dict:

        return {

            "prediction": self.prediction,

            "risk": self.risk.to_dict(),

            "shell": self.shell.to_dict(),

            "explanation": self.explanation.to_dict(),

            "recommendation": self.recommendation.to_dict(),
        }