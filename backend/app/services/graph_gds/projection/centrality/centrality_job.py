"""
==========================================================
AML Investigation Platform

Centrality Job

Responsibilities
----------------
✓ Ensure graph projection exists
✓ Execute selected GDS algorithms
✓ Persist centrality metrics
✓ Measure execution time

==========================================================
"""

from __future__ import annotations

import time

from app.models.graph_gds.centrality_execution_plan import (
    CentralityExecutionPlan,
)

from app.models.graph_gds.centrality_job_result import (
    CentralityJobResult,
)

from app.services.graph_gds.projection.centrality.centrality_repository import (
    CentralityRepository,
)

from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)


class CentralityJob:

    """
    Executes Neo4j Graph Data Science
    centrality algorithms.
    """

    def __init__(
        self,
        projection_service: GraphProjectionService,
        repository: CentralityRepository,
    ):

        self._projection_service = projection_service

        self._repository = repository

    def execute(
        self,
        plan: CentralityExecutionPlan | None = None,
    ) -> CentralityJobResult:

        if plan is None:

            plan = CentralityExecutionPlan()

        start_time = time.perf_counter()

        projection = self._projection_service.ensure_projection()

        degree_written = 0
        betweenness_written = 0
        closeness_written = 0
        pagerank_written = 0

        if plan.run_degree:

            degree_written = self._repository.run_degree(
                projection.graph_name
            )

        if plan.run_betweenness:

            betweenness_written = (
                self._repository.run_betweenness(
                    projection.graph_name
                )
            )

        if plan.run_closeness:

            closeness_written = (
                self._repository.run_closeness(
                    projection.graph_name
                )
            )

        if plan.run_pagerank:

            pagerank_written = (
                self._repository.run_pagerank(
                    projection.graph_name
                )
            )

        execution_time = (
            time.perf_counter() - start_time
        )

        return CentralityJobResult(

            graph_name=projection.graph_name,

            degree_written=degree_written,

            betweenness_written=betweenness_written,

            closeness_written=closeness_written,

            pagerank_written=pagerank_written,

            execution_time_seconds=round(
                execution_time,
                3,
            ),

            successful=True,
        )