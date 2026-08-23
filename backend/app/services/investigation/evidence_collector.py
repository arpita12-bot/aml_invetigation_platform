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
import traceback
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


class EvidenceCollector:
    """
    Collects all evidence required for
    an AML investigation.
    """

    def __init__(
        self,
        path_job: PathJob,
        shell_materializer: ShellPatternMaterializer,
    ):

        self._path_job = path_job
        self._shell_materializer = shell_materializer

    # =====================================================
    # Public API
    # =====================================================

    def collect(
        self,
        request: InvestigationRequest,
    ) -> InvestigationContext:
        """
        Execute all evidence collection
        for a single investigation.
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

            print("\n========== PATH ANALYTICS ERROR ==========")
            import traceback
            traceback.print_exc()
            print("==========================================")

            context.errors.append(

                f"Path Analytics: {type(exc).__name__}: {exc}"

            )

        # -------------------------------------------------
        # Shell Intelligence
        # -------------------------------------------------

        try:

            materialization = (

                self._shell_materializer.execute(

                    scope=request.scope,

                )

            )

            context.investigation_graph = (

                materialization.investigation_graph

            )

            context.shell_result = (

                materialization.shell_result

            )

        except Exception as exc:

            print("\n========== SHELL DETECTION ERROR ==========")
            import traceback
            traceback.print_exc()
            print("==========================================")

            context.errors.append(

                f"Shell Detection: {type(exc).__name__}: {exc}"

            )

        # -------------------------------------------------
        # Merge Warnings
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