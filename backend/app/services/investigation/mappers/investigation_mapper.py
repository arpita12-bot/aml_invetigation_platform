"""
==========================================================
AML Investigation Platform

Investigation Mapper

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.investigation_response_dto import (
    InvestigationResponseDTO,
)

from app.models.investigation.investigation_context import (
    InvestigationContext,
)

from app.services.investigation.mappers.graph_mapper import (
    GraphMapper,
)

from app.services.investigation.mappers.path_mapper import (
    PathMapper,
)

from app.services.investigation.mappers.shell_candidate_mapper import (
    ShellCandidateMapper,
)


class InvestigationMapper:
    """
    Converts InvestigationContext into
    InvestigationResponseDTO.
    """

    @staticmethod
    def map(
        context: InvestigationContext,
    ) -> InvestigationResponseDTO:

        graph = context.investigation_graph
        shell = context.shell_result
        path = context.path_result

        response = InvestigationResponseDTO(

            case_id=context.request.case_id,

            successful=not context.errors,

            execution_time_seconds=
                shell.execution_time_seconds
                if shell
                else 0,

            graph_nodes=
                GraphMapper.map_nodes(graph)
                if graph
                else [],

            graph_relationships=
                GraphMapper.map_relationships(graph)
                if graph
                else [],

            shell_candidates=
                ShellCandidateMapper.map_candidates(
                    shell.candidates
                )
                if shell
                else [],

            path_summary=
                PathMapper.map(path)
                if path
                else None,

            warnings=context.warnings,

            errors=context.errors,
        )

        # ---------------------------------------------------------
        # Investigation Intelligence
        # ---------------------------------------------------------

        if context.intelligence is not None:

            response.risk_score = (
                context.intelligence.risk_score.total_score
            )

            response.risk_level = (
                context.intelligence.risk_score.level
            )

            response.explanations = list(
                context.intelligence.explanations
            )

            response.recommendations = list(
                context.intelligence.recommendations
            )

        else:

            response.risk_score = 0.0

            response.risk_level = "UNKNOWN"

            response.explanations = []

            response.recommendations = []

        return response