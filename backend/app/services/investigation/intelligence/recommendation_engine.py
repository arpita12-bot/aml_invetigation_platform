"""
==========================================================
AML Investigation Platform

Recommendation Engine

==========================================================
"""

from __future__ import annotations

from app.models.risk.risk_score import (
    RiskScore,
)


class RecommendationEngine:

    """
    Produces investigation recommendations.
    """

    def recommend(
        self,
        risk_score: RiskScore,
    ) -> list[str]:

        recommendations: list[str] = []

        if risk_score.level == "LOW":

            recommendations.append(

                "Continue routine monitoring."

            )

        elif risk_score.level == "MEDIUM":

            recommendations.append(

                "Review recent transactions."

            )

            recommendations.append(

                "Perform customer due diligence."

            )

        elif risk_score.level == "HIGH":

            recommendations.append(

                "Escalate to AML analyst."

            )

            recommendations.append(

                "Perform Enhanced Due Diligence."

            )

        else:

            recommendations.append(

                "Immediate investigation required."

            )

            recommendations.append(

                "Consider SAR filing."

            )

            recommendations.append(

                "Review account restrictions."

            )

        return recommendations