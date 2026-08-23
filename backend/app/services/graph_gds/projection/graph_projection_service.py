"""
==========================================================
AML Investigation Platform

Graph Projection Service

Responsibilities
----------------
✓ Ensure graph projection exists
✓ Refresh graph projection
✓ Drop graph projection
✓ Retrieve graph metadata

==========================================================
"""

from __future__ import annotations

from app.models.graph_gds.graph_projection import GraphProjection

from app.services.graph_gds.projection.graph_projection_repository import (
    GraphProjectionRepository,
)

from app.services.graph_gds.projection.projection_constants import (
    GRAPH_NAME,
    DEFAULT_NODE_LABELS,
    DEFAULT_RELATIONSHIP_TYPES,
)


class GraphProjectionService:
    """
    Orchestrates Neo4j Graph Projection lifecycle.
    """

    def __init__(
        self,
        repository: GraphProjectionRepository,
    ):

        self._repository = repository

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def ensure_projection(self) -> GraphProjection:
        """
        Ensure that the graph projection exists.

        Creates it if necessary.
        """

        if self._repository.projection_exists(GRAPH_NAME):

            projection = self._repository.projection_info(
                GRAPH_NAME
            )

            if projection is None:

                raise RuntimeError(
                    "Projection exists but metadata could not be loaded."
                )

            return projection

        return self._repository.create_projection(

            graph_name=GRAPH_NAME,

            node_labels=DEFAULT_NODE_LABELS,

            relationship_types=DEFAULT_RELATIONSHIP_TYPES,
        )

    def refresh_projection(self) -> GraphProjection:
        """
        Rebuild the graph projection.

        Useful after graph synchronization.
        """

        if self._repository.projection_exists(GRAPH_NAME):

            self._repository.drop_projection(GRAPH_NAME)

        return self._repository.create_projection(

            graph_name=GRAPH_NAME,

            node_labels=DEFAULT_NODE_LABELS,

            relationship_types=DEFAULT_RELATIONSHIP_TYPES,
        )

    def drop_projection(self) -> bool:
        """
        Remove the projection if it exists.
        """

        if not self._repository.projection_exists(GRAPH_NAME):

            return True

        return self._repository.drop_projection(
            GRAPH_NAME
        )

    def get_projection(self) -> GraphProjection | None:
        """
        Return projection metadata.
        """

        return self._repository.projection_info(
            GRAPH_NAME
        )

    def projection_exists(self) -> bool:
        """
        Check whether projection exists.
        """

        return self._repository.projection_exists(
            GRAPH_NAME
        )