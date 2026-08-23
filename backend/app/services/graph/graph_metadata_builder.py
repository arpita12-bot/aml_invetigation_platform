"""
==========================================================
AML Investigation Platform

Graph Metadata Builder

Responsibilities
----------------
✓ Combine entities
✓ Combine relationships
✓ Build graph statistics
✓ Build graph indexes
✓ Produce GraphMetadata

==========================================================
"""

from __future__ import annotations

from collections import Counter, defaultdict

from app.models.graph.entity_metadata import EntityMetadata
from app.models.graph.graph_metadata import GraphMetadata
from app.models.schema.relationship_metadata import (
    RelationshipMetadata,
)


class GraphMetadataBuilder:

    @classmethod
    def build(
        cls,
        *,
        graph_name: str,
        source_dataset: str,
        entities: list[EntityMetadata],
        relationships: list[RelationshipMetadata],
    ) -> GraphMetadata:
        """
        Build enterprise graph metadata with lookup indexes.
        """

        # --------------------------------------------------
        # Graph Statistics
        # --------------------------------------------------

        entity_counter = Counter(
            entity.entity_type
            for entity in entities
        )

        relationship_counter = Counter(
            relationship.relationship_type
            for relationship in relationships
        )

        # --------------------------------------------------
        # Build Lookup Indexes
        # --------------------------------------------------

        entities_by_label: dict[
            str,
            list[EntityMetadata],
        ] = defaultdict(list)

        entities_by_identifier: dict[
            tuple[str, str],
            EntityMetadata,
        ] = {}

        for entity in entities:

            # Group by Neo4j label
            entities_by_label[
                entity.node_label
            ].append(entity)

            # Fast lookup using entity label
            key = (
                entity.node_label,
                entity.label,
            )

            if key not in entities_by_identifier:
                entities_by_identifier[key] = entity
        # --------------------------------------------------
        # Build GraphMetadata
        # --------------------------------------------------

        return GraphMetadata(

            graph_name=graph_name,

            source_dataset=source_dataset,

            entities=entities,

            relationships=relationships,

            entities_by_label=dict(
                entities_by_label
            ),

            entities_by_identifier=
                entities_by_identifier,

            node_count=len(entities),

            edge_count=len(relationships),

            entity_types=dict(
                entity_counter
            ),

            relationship_types=dict(
                relationship_counter
            ),

        )