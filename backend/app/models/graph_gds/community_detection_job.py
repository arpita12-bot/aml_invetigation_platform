"""
==========================================================
AML Investigation Platform

Community Detection Job

Responsibilities
----------------
✓ Ensure graph projection exists
✓ Execute Louvain
✓ Persist community IDs

==========================================================
"""

from __future__ import annotations

from app.models.graph_gds.community_job_result import (
    CommunityJobResult,
)

from app.models.graph_gds.community_repository import (
    CommunityRepository,
)

from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)


class CommunityDetectionJob:

    """
    Executes Louvain community detection.
    """

    def __init__(

        self,

        projection_service: GraphProjectionService,

        repository: CommunityRepository,

    ):

        self._projection_service = projection_service

        self._repository = repository

    def execute(self) -> CommunityJobResult:

        projection = self._projection_service.ensure_projection()

        return self._repository.run_louvain(

            projection.graph_name
        )