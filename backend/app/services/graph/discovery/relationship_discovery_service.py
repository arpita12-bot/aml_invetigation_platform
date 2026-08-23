"""
==========================================================
AML Investigation Platform

Relationship Discovery Engine

Responsibilities
----------------
✓ Coordinate relationship discovery
✓ Aggregate all discovery providers
✓ Validate relationships
✓ Remove duplicates
✓ Return final relationship metadata

==========================================================
"""

from __future__ import annotations

from typing import Dict, List

from app.models.schema.relationship_metadata import RelationshipMetadata
from app.models.schema.table_metadata import TableMetadata

from app.services.graph.discovery.metadata_cache import MetadataCache
from app.services.graph.discovery.foreign_key_provider import ForeignKeyProvider
from app.services.graph.discovery.relationship_validator import (
    RelationshipValidator,
)
from app.services.graph.discovery.relationship_deduplicator import (
    RelationshipDeduplicator,
)


class RelationshipDiscoveryService:
    """
    Coordinates relationship discovery.

    The engine itself contains no discovery logic.
    """

    def __init__(
        self,
        foreign_key_provider: ForeignKeyProvider | None = None,
        validator: RelationshipValidator | None = None,
        deduplicator: RelationshipDeduplicator | None = None,
    ):

        self.foreign_key_provider = (
            foreign_key_provider
            or ForeignKeyProvider()
        )

        self.validator = (
            validator
            or RelationshipValidator()
        )

        self.deduplicator = (
            deduplicator
            or RelationshipDeduplicator()
        )

    # =====================================================

    def discover(
        self,
        cache: MetadataCache,
        tables: Dict[str, TableMetadata],
    ) -> List[RelationshipMetadata]:

        cache.load()

        relationships: List[RelationshipMetadata] = []

        # ----------------------------------------
        # Foreign Key Discovery
        # ----------------------------------------

        relationships.extend(
            self.foreign_key_provider.discover(cache)
        )

        # ----------------------------------------
        # Schema Relationships
        # ----------------------------------------

        relationships.extend(
            relationship
            for table in tables.values()
            for relationship in table.relationships
        )

        # ----------------------------------------
        # Validation
        # ----------------------------------------

        relationships = self.validator.validate(
            relationships=relationships,
            cache=cache,
            tables=tables,
        )

        # ----------------------------------------
        # Deduplication
        # ----------------------------------------

        relationships = self.deduplicator.deduplicate(
            relationships
        )

        return relationships