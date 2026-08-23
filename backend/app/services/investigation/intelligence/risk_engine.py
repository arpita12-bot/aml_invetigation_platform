"""
==========================================================
AML Investigation Platform

Risk Engine

==========================================================
"""

from __future__ import annotations

import time

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_score import RiskScore
from app.models.risk.risk_scoring_result import RiskScoringResult

from app.services.risk.graph_analytics_engine import (
    GraphAnalyticsEngine,
)


class RiskEngine:

    @classmethod
    def calculate(
        cls,
        graph: GraphMetadata,
    ) -> RiskScoringResult:

        start = time.perf_counter()

        factors = GraphAnalyticsEngine.analyze(graph)

        if factors:

            total_weight = sum(
                factor.weight
                for factor in factors
            )

            weighted_score = sum(
                factor.score * factor.weight
                for factor in factors
            )

            overall_score = (
                weighted_score / total_weight
                if total_weight > 0
                else 0.0
            )

        else:

            overall_score = 0.0

        # ----------------------------------
        # Determine AML Risk Level
        # ----------------------------------

        if overall_score >= 80:

            level = "CRITICAL"

        elif overall_score >= 60:

            level = "HIGH"

        elif overall_score >= 40:

            level = "MEDIUM"

        elif overall_score >= 20:

            level = "LOW"

        else:

            level = "MINIMAL"

        elapsed = time.perf_counter() - start

        risk_score = RiskScore(

            total_score=round(overall_score, 2),

            level=level,

            factors=factors,

        )

        return RiskScoringResult(

            risk_score=risk_score,

            factors=factors,

            execution_time_seconds=round(elapsed, 3),

            successful=True,

        )