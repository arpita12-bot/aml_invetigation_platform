"""
==========================================================
AML Investigation Platform

Investigation Report Builder

Responsibilities
----------------
✓ Build investigation report
✓ Calculate overall investigation risk
✓ Generate executive summary

==========================================================
"""

from __future__ import annotations

from app.models.investigation.investigation_context import (
    InvestigationContext,
)

from app.models.investigation.investigation_report import (
    InvestigationReport,
)

from app.models.recommendation import (
    Recommendation,
)

class InvestigationReportBuilder:
    """
    Builds the final AML investigation report.
    """

    def build(
        self,
        context: InvestigationContext,
        recommendations: list[Recommendation],
    ) -> InvestigationReport:

        shell_candidates = []

        execution_time = 0.0

        if context.shell_result:

            shell_candidates = context.shell_result.candidates

            execution_time += (
                context.shell_result.execution_time_seconds
            )

        if context.path_result:

            execution_time += (
                context.path_result.execution_time_seconds
            )

        risk_score = self._calculate_risk(shell_candidates)

        risk_level = self._risk_level(risk_score)

        summary = self._summary(
            context,
            risk_level,
            risk_score,
            shell_candidates,
        )

        successful = len(context.errors) == 0

        return InvestigationReport(

            case_id=context.request.case_id,

            entity_id=context.request.entity_id,

            entity_type=context.request.entity_type,

            analyst=context.request.analyst,

            risk_level=risk_level,

            risk_score=risk_score,

            summary=summary,

            shell_candidates=shell_candidates,

            recommendations=recommendations,

            execution_time_seconds=round(
                execution_time,
                3,
            ),

            successful=successful,

            warnings=context.warnings,

            errors=context.errors,

        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _calculate_risk(
        candidates,
    ) -> float:

        if not candidates:

            return 0.0

        return round(

            max(

                c.suspicion_score

                for c in candidates

            ),

            3,

        )

    @staticmethod
    def _risk_level(
        score: float,
    ) -> str:

        if score >= 0.90:

            return "VERY HIGH"

        if score >= 0.75:

            return "HIGH"

        if score >= 0.60:

            return "MEDIUM"

        if score >= 0.40:

            return "LOW"

        return "MINIMAL"

    @staticmethod
    def _summary(

        context: InvestigationContext,

        risk_level: str,

        score: float,

        candidates,

    ) -> str:

        return (

            f"Investigation for "

            f"{context.request.entity_type} "

            f"'{context.request.entity_id}' "

            f"completed successfully. "

            f"Overall Risk: {risk_level} "

            f"(Score: {score:.2f}). "

            f"Potential shell companies identified: "

            f"{len(candidates)}."

        )