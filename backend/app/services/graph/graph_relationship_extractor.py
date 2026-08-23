"""
==========================================================
AML Investigation Platform

Graph Relationship Extractor

Responsibilities
----------------
✓ Entry point for relationship discovery
✓ Load metadata cache
✓ Delegate relationship discovery
✓ Return validated relationship metadata

Notes
-----
This class intentionally contains no discovery logic.
All relationship discovery is handled by:

- MetadataCache
- ForeignKeyProvider
- RelationshipDiscoveryService
- RelationshipValidator
- RelationshipDeduplicator

==========================================================
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.models.schema.relationship_metadata import (
    RelationshipMetadata,
)
from app.models.schema.table_metadata import TableMetadata

from app.services.graph.discovery.metadata_cache import (
    MetadataCache,
)
from backend.app.services.graph.discovery.relationship_discovery_service import (
    RelationshipDiscoveryService,
)

logger = logging.getLogger(__name__)


class GraphRelationshipExtractor:
    """
    Thin façade responsible for orchestrating relationship
    discovery.

    It does not perform discovery itself.
    """

    def __init__(
        self,
        db: Session,
        discovery_engine: RelationshipDiscoveryService | None = None,
    ):

        self.db = db

        self.metadata_cache = MetadataCache(db)

        self.discovery_engine = (
            discovery_engine
            or RelationshipDiscoveryService()
        )

    # =====================================================
    # Public API
    # =====================================================

    def extract_relationships(
        self,
        tables: dict[str, TableMetadata],
    ) -> list[RelationshipMetadata]:
        """
        Discover all graph relationships.

        Parameters
        ----------
        tables:
            Dictionary of TableMetadata keyed by table name.

        Returns
        -------
        List[RelationshipMetadata]
        """

        logger.info(
            "Starting relationship discovery..."
        )

        relationships = self.discovery_engine.discover(
            cache=self.metadata_cache,
            tables=tables,
        )

        logger.info(
            "Relationship discovery completed. %d relationships discovered.",
            len(relationships),
        )

        return relationships

    # =====================================================
    # Convenience Helpers
    # =====================================================

    def extract_for_table(
        self,
        table_name: str,
        tables: dict[str, TableMetadata],
    ) -> list[RelationshipMetadata]:
        """
        Return relationships involving a single table.
        """

        relationships = self.extract_relationships(
            tables
        )

        return [

            relationship

            for relationship in relationships

            if (
                relationship.source_table == table_name
                or relationship.target_table == table_name
            )

        ]

    def relationship_count(
        self,
        tables: dict[str, TableMetadata],
    ) -> int:

        return len(
            self.extract_relationships(
                tables
            )
        )

    def has_relationships(
        self,
        tables: dict[str, TableMetadata],
    ) -> bool:

        return self.relationship_count(
            tables
        ) > 0