"""
==========================================================
AML Investigation Platform

Investigation Recommender

Responsibilities
----------------

✓ Generate investigation actions
✓ Determine investigation priority
✓ Recommend EDD
✓ Recommend SAR
✓ Recommend account freeze
✓ Recommend compliance escalation

==========================================================
"""

from __future__ import annotations

from app.models.aml.investigation_recommendation import (
    InvestigationRecommendation,
)
from app.models.aml.risk_score import RiskScore
from app.models.aml.shell_company_assessment import (
    ShellCompanyAssessment,
)


class InvestigationRecommender:

    """
    Generates investigator actions from AML intelligence.
    """

    def recommend(
        self,
        *,
        risk: RiskScore,
        shell: ShellCompanyAssessment,
    ) -> InvestigationRecommendation:

        score = risk.total_score
        shell_score = shell.shell_score

        # ----------------------------------
        # Critical
        # ----------------------------------

        if score >= 90 and shell_score >= 90:

            return InvestigationRecommendation(

                priority="CRITICAL",

                action=(
                    "Immediate investigation required."
                ),

                explanation=(
                    "Very high AML risk combined with "
                    "strong shell company indicators."
                ),

                requires_edd=True,

                requires_sar=True,

                freeze_account=True,

                notify_compliance=True,
            )

        # ----------------------------------
        # High
        # ----------------------------------

        if score >= 80 and shell_score >= 80:

            return InvestigationRecommendation(

                priority="HIGH",

                action=(
                    "Open AML investigation."
                ),

                explanation=(
                    "High AML risk with multiple shell "
                    "company indicators."
                ),

                requires_edd=True,

                requires_sar=True,

                freeze_account=False,

                notify_compliance=True,
            )

        # ----------------------------------
        # Medium
        # ----------------------------------

        if score >= 65:

            return InvestigationRecommendation(

                priority="MEDIUM",

                action=(
                    "Perform analyst review."
                ),

                explanation=(
                    "Moderate AML indicators detected."
                ),

                requires_edd=True,

                requires_sar=False,

                freeze_account=False,

                notify_compliance=True,
            )

        # ----------------------------------
        # Low
        # ----------------------------------

        return InvestigationRecommendation(

            priority="LOW",

            action=(
                "Continue monitoring."
            ),

            explanation=(
                "Current evidence is insufficient for "
                "further escalation."
            ),

            requires_edd=False,

            requires_sar=False,

            freeze_account=False,

            notify_compliance=False,
        )