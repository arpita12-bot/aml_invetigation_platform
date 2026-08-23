"""
==========================================================
AML Investigation Platform

Graph Sync Service

Responsibilities
----------------
✓ Populate GraphMetadata
✓ Load Neo4j
✓ Refresh GDS Projection

==========================================================
"""

from sqlalchemy.orm import Session

from app.models.schema.dataset_metadata import DatasetMetadata

from app.services.graph.graph_metadata_populator import (
    GraphMetadataPopulator,
)

from app.services.graph.neo4j.graph_loader import (
    GraphLoader,
)

from app.services.graph.neo4j.graph_projection_service import (
    GraphProjectionService,
)


class GraphSyncService:

    @classmethod
    def synchronize(
        cls,
        *,
        session: Session,
        metadata: DatasetMetadata,
    ):

        metadata = GraphMetadataPopulator.populate(
            session=session,
            metadata=metadata,
        )

        loader = GraphLoader()

        result = loader.load(
            metadata.graph
        )

        GraphProjectionService.refresh_projection()

        return result