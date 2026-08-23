"""
==========================================================
AML Investigation Platform

Investigation Intelligence Job

Responsibilities
----------------
✓ Calculate investigation risk
✓ Generate explanations
✓ Produce recommendations
✓ Aggregate investigation intelligence

==========================================================
"""

from __future__ import annotations

import time

from app.models.investigation.investigation_context import (
    InvestigationContext,
)

from app.models.investigation.investigation_intelligence_result import (
    InvestigationIntelligenceResult,
)

from app.services.investigation.intelligence.risk_engine import (
    RiskEngine,
)

from app.services.investigation.intelligence.explainability_engine import (
    ExplainabilityEngine,
)

from app.services.investigation.intelligence.recommendation_engine import (
    RecommendationEngine,
)


class InvestigationIntelligenceJob:

    def __init__(
        self,
        risk_engine: RiskEngine,
        explainability_engine: ExplainabilityEngine,
        recommendation_engine: RecommendationEngine,
    ):

        self._risk_engine = risk_engine

        self._explainability_engine = explainability_engine

        self._recommendation_engine = recommendation_engine

    # -----------------------------------------------------

    def execute(
        self,
        context: InvestigationContext,
    ) -> InvestigationIntelligenceResult:

        start = time.perf_counter()

        risk = self._risk_engine.calculate(context)

        explanations = (
            self._explainability_engine.build(context)
        )

        recommendations = (
            self._recommendation_engine.recommend(risk)
        )

        return InvestigationIntelligenceResult(

            risk_score=risk,

            explanations=explanations,

            recommendations=recommendations,

            execution_time_seconds=round(

                time.perf_counter() - start,

                3,

            ),

            successful=True,
        )