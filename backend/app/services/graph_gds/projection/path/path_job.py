"""
==========================================================
AML Investigation Platform

Path Analytics Job

Responsibilities
----------------
✓ Ensure graph projection exists
✓ Execute path repositories
✓ Aggregate investigation paths
✓ Return unified result

==========================================================
"""

from __future__ import annotations

import time

from app.models.graph_gds.path_execution_plan import (
    PathExecutionPlan,
)

from app.models.graph_gds.path_job_result import (
    PathJobResult,
)

from app.models.investigation.investigation_scope import (
    InvestigationScope,
)

from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)

from app.services.graph_gds.projection.path.repositories.pep_path_repository import (
    PepPathRepository,
)

from app.services.graph_gds.projection.path.repositories.sanction_path_repository import (
    SanctionPathRepository,
)

from app.services.graph_gds.projection.path.repositories.ownership_path_repository import (
    OwnershipPathRepository,
)

from app.services.graph_gds.projection.path.repositories.shell_path_repository import (
    ShellPathRepository,
)


class PathJob:
    """
    Executes all graph path analytics
    for one investigation.
    """

    def __init__(
        self,
        projection_service: GraphProjectionService,
        pep_repository: PepPathRepository,
        sanction_repository: SanctionPathRepository,
        ownership_repository: OwnershipPathRepository,
        shell_repository: ShellPathRepository,
    ):

        self._projection_service = projection_service

        self._pep_repository = pep_repository

        self._sanction_repository = sanction_repository

        self._ownership_repository = ownership_repository

        self._shell_repository = shell_repository

    # =====================================================
    # Public API
    # =====================================================

    def execute(
        self,
        scope: InvestigationScope,
        plan: PathExecutionPlan | None = None,
    ) -> PathJobResult:
        """
        Execute all path analytics for
        the supplied investigation scope.
        """

        if plan is None:

            plan = PathExecutionPlan()

        start = time.perf_counter()

        projection = (
            self._projection_service.ensure_projection()
        )

        result = PathJobResult(
            graph_name=projection.graph_name,
        )

        entity_id = scope.entity_id

        max_depth = scope.max_depth

        # -------------------------------------------------
        # PEP Paths
        # -------------------------------------------------

        try:

            if (
                scope.include_pep
                and plan.compute_pep_paths
            ):

                result.pep_paths = (

                    self._pep_repository.find_pep_paths(

                        entity_id,

                        max_depth=max_depth,

                    )

                )

        except Exception as exc:

            result.errors.append(

                f"PEP Paths: {exc}"

            )

        # -------------------------------------------------
        # Sanction Paths
        # -------------------------------------------------

        try:

            if (
                scope.include_sanctions
                and plan.compute_sanction_paths
            ):

                result.sanction_paths = (

                    self._sanction_repository.find_sanction_paths(

                        entity_id,

                        max_depth=max_depth,

                    )

                )

        except Exception as exc:

            result.errors.append(

                f"Sanction Paths: {exc}"

            )

        # -------------------------------------------------
        # Ownership Paths
        # -------------------------------------------------

        try:

            if plan.compute_ownership_paths:

                result.ownership_paths = (

                    self._ownership_repository.find_ownership_paths(

                        entity_id,

                        max_depth=max_depth,

                    )

                )

        except Exception as exc:

            result.errors.append(

                f"Ownership Paths: {exc}"

            )

        # -------------------------------------------------
        # Shell Company Paths
        # -------------------------------------------------

        try:

            result.shell_paths = (

                self._shell_repository.find_shell_company_paths(

                    entity_id,

                    max_depth=max_depth,

                )

            )

        except Exception as exc:

            result.errors.append(

                f"Shell Paths: {exc}"

            )

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        result.execution_time_seconds = round(

            time.perf_counter() - start,

            3,

        )

        result.successful = (

            len(result.errors) == 0

        )

        return result