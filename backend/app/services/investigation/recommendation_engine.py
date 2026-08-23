"""
==========================================================
AML Investigation Platform

Recommendation Engine

Responsibilities
----------------
✓ Generate investigator recommendations
✓ Determine overall investigation risk
✓ Prioritize next actions

==========================================================
"""

from __future__ import annotations

from app.models.investigation.investigation_context import (
    InvestigationContext,
)

from app.models.recommendation import (
    Recommendation,
)

class RecommendationEngine:

    """
    Generates AML investigation recommendations.
    """

    def generate(
        self,
        context: InvestigationContext,
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        shell_result = context.shell_result

        if shell_result:

            for candidate in shell_result.candidates[:10]:

                score = candidate.suspicion_score

                # -------------------------------------------------
                # Very High Risk
                # -------------------------------------------------

                if score >= 0.90:

                    recommendations.extend(

                        [

                            Recommendation(

                                priority=1,

                                category="Escalation",

                                title="Immediate AML Escalation",

                                description=(
                                    f"{candidate.company_name} "
                                    "shows extremely high shell "
                                    "company indicators."
                                ),

                                mandatory=True,

                            ),

                            Recommendation(

                                priority=1,

                                category="Enhanced Due Diligence",

                                title="Perform Enhanced Due Diligence",

                                description=(
                                    "Validate beneficial ownership, "
                                    "corporate structure, "
                                    "and source of funds."
                                ),

                                mandatory=True,

                            ),

                        ]

                    )

                # -------------------------------------------------
                # High Risk
                # -------------------------------------------------

                elif score >= 0.75:

                    recommendations.append(

                        Recommendation(

                            priority=2,

                            category="Manual Review",

                            title="Senior AML Review",

                            description=(
                                f"Review investigation for "
                                f"{candidate.company_name}."
                            ),

                            mandatory=True,

                        )

                    )

                # -------------------------------------------------
                # Medium Risk
                # -------------------------------------------------

                elif score >= 0.60:

                    recommendations.append(

                        Recommendation(

                            priority=3,

                            category="Monitoring",

                            title="Increase Monitoring",

                            description=(
                                "Increase transaction monitoring "
                                "frequency."
                            ),

                        )

                    )

                # -------------------------------------------------
                # PEP
                # -------------------------------------------------

                if candidate.pep_score > 0:

                    recommendations.append(

                        Recommendation(

                            priority=2,

                            category="PEP",

                            title="Review PEP Exposure",

                            description=(
                                "Verify relationship with "
                                "Politically Exposed Persons."
                            ),

                        )

                    )

                # -------------------------------------------------
                # Sanctions
                # -------------------------------------------------

                if candidate.sanction_score > 0:

                    recommendations.append(

                        Recommendation(

                            priority=1,

                            category="Sanctions",

                            title="Sanctions Screening",

                            description=(
                                "Review sanction-related "
                                "connections immediately."
                            ),

                            mandatory=True,

                        )

                    )

                # -------------------------------------------------
                # Ownership
                # -------------------------------------------------

                if candidate.ownership_score > 0.60:

                    recommendations.append(

                        Recommendation(

                            priority=2,

                            category="Ownership",

                            title="Investigate Ownership Chain",

                            description=(
                                "Review beneficial ownership "
                                "across multiple corporate layers."
                            ),

                        )

                    )

        recommendations.sort(key=lambda x: x.priority)

        return self._remove_duplicates(recommendations)

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _remove_duplicates(
        recommendations: list[Recommendation],
    ) -> list[Recommendation]:

        seen = set()

        unique = []

        for item in recommendations:

            key = (

                item.category,

                item.title,

            )

            if key not in seen:

                seen.add(key)

                unique.append(item)

        return unique