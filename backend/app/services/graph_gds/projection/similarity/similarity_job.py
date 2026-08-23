import time

from app.models.graph_gds.similarity_execution_plan import (
    SimilarityExecutionPlan,
)

from app.models.graph_gds.similarity_job_result import (
    SimilarityJobResult,
)

from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)

from app.services.graph_gds.projection.similarity.similarity_repository import (
    SimilarityRepository,
)


class SimilarityJob:

    def __init__(

        self,

        projection_service: GraphProjectionService,

        repository: SimilarityRepository,

    ):

        self._projection_service = projection_service

        self._repository = repository

    def execute(

        self,

        plan: SimilarityExecutionPlan | None = None,

    ) -> SimilarityJobResult:

        if plan is None:

            plan = SimilarityExecutionPlan()

        start = time.perf_counter()

        projection = (
            self._projection_service.ensure_projection()
        )

        relationships, pairs = (
            self._repository.run_node_similarity(

                graph_name=projection.graph_name,

                similarity_threshold=plan.similarity_threshold,

                top_k=plan.top_k,
            )
        )

        return SimilarityJobResult(

            graph_name=projection.graph_name,

            relationships_written=relationships,

            similarity_pairs=pairs,

            execution_time_seconds=round(

                time.perf_counter() - start,

                3,
            ),

            successful=True,
        )