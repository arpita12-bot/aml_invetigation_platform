"""
==========================================================
AML Investigation Platform

Neo4j Graph Loader

Responsibilities
----------------
✓ Create constraints
✓ Load nodes
✓ Load relationships
✓ Track execution metrics
✓ Return GraphSyncResult

==========================================================
"""

from __future__ import annotations

import time
from datetime import datetime

from app.models.graph.graph_metadata import GraphMetadata
from app.models.graph.graph_sync_result import GraphSyncResult

from app.services.graph.neo4j.constraint_manager import (
    ConstraintManager,
)
from app.services.graph.neo4j.node_loader import NodeLoader
from app.services.graph.neo4j.relationship_loader import (
    RelationshipLoader,
)
import logging

logger = logging.getLogger(__name__)

class GraphLoader:

    @classmethod
    def load(
        cls,
        *,
        session,
        graph: GraphMetadata,
        batch_size: int = 5000,
    ) -> GraphSyncResult:
        """
        Load an entire graph into Neo4j.
        """

        result = GraphSyncResult(
            graph_name=graph.graph_name,
            started_at=datetime.utcnow(),
        )

        start = time.perf_counter()

        try:

            # -----------------------------------------
            # Create Constraints
            # -----------------------------------------

            constraints_created = ConstraintManager.create_constraints(
                session=session,
                graph=graph,
            )

            indexes_created = ConstraintManager.create_indexes(
                session=session,
                graph=graph,
            )

            result.constraints_created = constraints_created
            result.indexes_created = indexes_created
            
            # -----------------------------------------
            # Load Nodes
            # -----------------------------------------

            nodes_loaded = NodeLoader.load(
                session=session,
                graph=graph,
                batch_size=batch_size,
            )

            result.nodes_loaded = nodes_loaded

            # -----------------------------------------
            # Load Relationships
            # -----------------------------------------

            relationships_loaded = RelationshipLoader.load(
                session=session,
                graph=graph,
                batch_size=batch_size,
            )

            result.relationships_loaded = relationships_loaded

            result.success = True

        except Exception as exc:

            logger.exception("Graph loading failed")

            result.success = False

            result.errors.append(str(exc))

        finally:

            result.finished_at = datetime.utcnow()

            result.execution_time_seconds = (
                time.perf_counter() - start
            )

        return result