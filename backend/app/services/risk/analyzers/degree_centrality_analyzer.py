"""
==========================================================
AML Investigation Platform

Degree Centrality Analyzer

Responsibilities
----------------
✓ Dataset independent
✓ GraphMetadata based
✓ Produces RiskFactor objects

==========================================================
"""

from __future__ import annotations

from collections import defaultdict

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor

from app.services.risk.analyzers.base_analyzer import (
    BaseAnalyzer,
)


class DegreeCentralityAnalyzer(BaseAnalyzer):

    HIGH_DEGREE_THRESHOLD = 10

    @classmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:

        degree = defaultdict(int)

        for relationship in graph.relationships:

            degree[
                (
                    relationship.source_label,
                    relationship.source_identifier_value,
                )
            ] += 1

            degree[
                (
                    relationship.target_label,
                    relationship.target_identifier_value,
                )
            ] += 1

        factors: list[RiskFactor] = []

        for (_, identifier), count in degree.items():

            if count < cls.HIGH_DEGREE_THRESHOLD:
                continue

            factors.append(

                RiskFactor(

                    name=f"High Degree ({identifier})",

                    score=min(count * 5, 100),

                    weight=0.25,

                    description=(
                        f"Entity participates in "
                        f"{count} relationships."
                    ),

                )

            )

        return factors