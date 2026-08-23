"""
==========================================================
AML Investigation Platform

Evidence Collector

Responsibilities
----------------
✓ Collect graph evidence
✓ Execute graph intelligence services
✓ Build investigation context

==========================================================
"""

from __future__ import annotations

from app.models.investigation.investigation_context import (
    InvestigationContext,
)

from app.models.investigation.investigation_request import (
    InvestigationRequest,
)

from app.services.graph_gds.projection.path.path_job import (
    PathJob,
)

from app.services.shell_detection.shell_pattern_materializer import (
    ShellPatternMaterializer,
)

from app.services.graph_gds.projection.centrality.repositories.centrality_reader_repository import (
    CentralityReaderRepository,
)


class EvidenceCollector:
    """
    Collects all evidence required for
    an AML investigation.
    """

    def __init__(
        self,
        path_job: PathJob,
        shell_materializer: ShellPatternMaterializer,
        centrality_reader: CentralityReaderRepository,
    ):

        self._path_job = path_job

        self._shell_materializer = shell_materializer

        self._centrality_reader = centrality_reader

    # =====================================================
    # Public API
    # =====================================================

    def collect(
        self,
        request: InvestigationRequest,
    ) -> InvestigationContext:
        """
        Collect all investigation evidence.
        """

        context = InvestigationContext(

            request=request,

        )

        # -------------------------------------------------
        # Path Analytics
        # -------------------------------------------------

        try:

            context.path_result = (

                self._path_job.execute(

                    scope=request.scope,

                )

            )

        except Exception as exc:

            context.errors.append(

                f"Path Analytics: {exc}"

            )
            
            
        # -------------------------------------------------
        # Graph Centrality
        # -------------------------------------------------

        try:

            context.centrality_metrics = (

                self._centrality_reader.find_customer_metrics(

                    request.scope.entity_id,

                )

            )

        except Exception as exc:

            print("\n========== CENTRALITY ERROR ==========")

            traceback.print_exc()

            print("======================================")

            context.errors.append(

                f"Centrality: {type(exc).__name__}: {exc}"

            )

        # -------------------------------------------------
        # Shell Intelligence
        # -------------------------------------------------

        try:

            context.shell_result = (

                self._shell_materializer.execute(

                    scope=request.scope,

                )

            )

        except Exception as exc:

            context.errors.append(

                f"Shell Detection: {exc}"

            )

        # -------------------------------------------------
        # Merge warnings
        # -------------------------------------------------

        if context.path_result:

            context.warnings.extend(

                context.path_result.warnings

            )

        if context.shell_result:

            context.warnings.extend(

                context.shell_result.warnings

            )

        return context