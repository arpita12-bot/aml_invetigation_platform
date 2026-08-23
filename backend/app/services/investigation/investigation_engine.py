"""
==========================================================
AML Investigation Platform

Investigation Engine

Responsibilities
----------------
✓ Orchestrate AML investigation
✓ Calculate graph risk
✓ Collect graph evidence
✓ Generate recommendations
✓ Build investigation report

==========================================================
"""

from __future__ import annotations

from app.models.graph.graph_metadata import GraphMetadata

from app.models.investigation.investigation_report import (
    InvestigationReport,
)

from app.models.investigation.investigation_request import (
    InvestigationRequest,
)

from app.services.investigation.evidence_collector import (
    EvidenceCollector,
)

from app.services.investigation.recommendation_engine import (
    RecommendationEngine,
)

from app.services.investigation.investigation_report_builder import (
    InvestigationReportBuilder,
)

from app.services.investigation.intelligence.risk_engine import (
    RiskEngine,
)


class InvestigationEngine:
    """
    Central orchestration service for AML investigations.
    """

    def __init__(
        self,
        risk_engine: RiskEngine,
        evidence_collector: EvidenceCollector,
        recommendation_engine: RecommendationEngine,
        report_builder: InvestigationReportBuilder,
    ):

        self._risk_engine = risk_engine
        self._evidence_collector = evidence_collector
        self._recommendation_engine = recommendation_engine
        self._report_builder = report_builder

    # ======================================================
    # Public API
    # ======================================================

    def investigate(
        self,
        request: InvestigationRequest,
        graph: GraphMetadata,
    ) -> InvestigationReport:

        # -----------------------------------------
        # Calculate Risk
        # -----------------------------------------

        risk_result = self._risk_engine.calculate(graph)

        # -----------------------------------------
        # Collect Evidence
        # -----------------------------------------

        evidence = self._evidence_collector.collect(
            graph=graph,
            request=request,
            risk_result=risk_result,
        )

        # -----------------------------------------
        # Generate Recommendations
        # -----------------------------------------

        recommendations = self._recommendation_engine.generate(
            evidence=evidence,
            risk_result=risk_result,
        )

        # -----------------------------------------
        # Build Final Report
        # -----------------------------------------

        report = self._report_builder.build(
            graph=graph,
            request=request,
            risk_result=risk_result,
            evidence=evidence,
            recommendations=recommendations,
        )

        return report