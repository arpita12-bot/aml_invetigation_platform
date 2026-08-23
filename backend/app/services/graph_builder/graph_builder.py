"""
==========================================================
AML Investigation Platform

Enterprise Graph Builder

Responsibilities
----------------
✓ Load graph nodes
✓ Load graph relationships
✓ Validate graph
✓ Generate graph statistics
✓ Refresh graph projection

==========================================================
"""

from __future__ import annotations

import logging

from app.services.graph.neo4j.node_loader import NodeLoader
from app.services.graph.neo4j.relationship_loader import (
    RelationshipLoader,
)
from app.services.graph_builder.graph_validator import (
    GraphValidator,
)
from app.services.graph_builder.graph_statistics import (
    GraphStatisticsService,
)

from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Main orchestrator responsible for synchronizing
    the complete AML Knowledge Graph.
    """

    def __init__(
        self,
        node_loader: NodeLoader,
        relationship_loader: RelationshipLoader,
        validator: GraphValidator,
        statistics: GraphStatisticsService,
        projection_service: GraphProjectionService,
    ):
        self._node_loader = node_loader
        self._relationship_loader = relationship_loader
        self._validator = validator
        self._statistics = statistics
        self._projection_service = projection_service

    def build(self) -> dict:
        """
        Complete graph synchronization workflow.
        """

        logger.info("=" * 60)
        logger.info("Starting Graph Build")
        logger.info("=" * 60)

        # -------------------------------------------------
        # Load Nodes
        # -------------------------------------------------

        self._node_loader.load_all()

        # -------------------------------------------------
        # Load Relationships
        # -------------------------------------------------

        self._relationship_loader.build_all()

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        validation = self._validator.validate()

        # -------------------------------------------------
        # Refresh GDS Projection
        # -------------------------------------------------

        projection = self._projection_service.refresh_projection()

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        stats = self._statistics.generate()

        logger.info("Graph build completed successfully.")

        return {
            "validation": validation,
            "projection": projection,
            "statistics": stats,
        }