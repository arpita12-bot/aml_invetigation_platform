"""
==========================================================
AML Investigation Platform

Community Risk Analyzer

Responsibilities
----------------
✓ Consume existing community detection output
✓ Produce RiskFactors
✓ Dataset independent

==========================================================
"""

from __future__ import annotations

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor

from app.services.risk.analyzers.base_analyzer import BaseAnalyzer


class CommunityAnalyzer(BaseAnalyzer):

    COMMUNITY_SIZE_THRESHOLD = 5

    @classmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:

        #
        # Placeholder
        #
        # Existing CommunityDetectionService
        # will be plugged here.
        #

        communities = []

        factors: list[RiskFactor] = []

        for community in communities:

            if len(community.members) < cls.COMMUNITY_SIZE_THRESHOLD:
                continue

            factors.append(

                RiskFactor(

                    name="Dense Community",

                    score=min(len(community.members) * 8, 100),

                    weight=0.20,

                    description=(
                        f"Community contains "
                        f"{len(community.members)} connected entities."
                    ),

                    entity_label=None,

                    entity_identifier=None,

                )

            )

        return factors