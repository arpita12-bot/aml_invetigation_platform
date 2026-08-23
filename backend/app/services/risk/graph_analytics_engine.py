"""
==========================================================
AML Investigation Platform

Graph Analytics Engine

Responsibilities
----------------
✓ Execute all graph analyzers
✓ Aggregate RiskFactor objects
✓ Never calculate overall score

==========================================================
"""

from __future__ import annotations

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor

from app.services.risk.analyzers.degree_centrality_analyzer import (
    DegreeCentralityAnalyzer,
)
from app.services.risk.analyzers.cycle_analyzer import (
    CycleAnalyzer,
)
from app.services.risk.analyzers.shared_identifier_analyzer import (
    SharedIdentifierAnalyzer,
)


class GraphAnalyticsEngine:

    ANALYZERS = [

        DegreeCentralityAnalyzer,

        CycleAnalyzer,

        SharedIdentifierAnalyzer,

    ]

    @classmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:

        factors: list[RiskFactor] = []

        for analyzer in cls.ANALYZERS:

            try:

                factors.extend(
                    analyzer.analyze(graph)
                )

            except Exception as ex:

                print(
                    f"{analyzer.__name__} failed: {ex}"
                )

        return factors