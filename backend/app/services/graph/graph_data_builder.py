"""
==========================================================
AML Investigation Platform

Graph Data Builder

Builds GraphMetadata from PostgreSQL datasets.

==========================================================
"""

from __future__ import annotations

from collections import defaultdict

from app.models.graph.entity_metadata import EntityMetadata
from app.models.graph.graph_metadata import GraphMetadata
from app.models.schema.relationship_metadata import RelationshipMetadata


class GraphDataBuilder:
    """
    Converts business records into GraphMetadata.
    """

    @classmethod
    def build(
        cls,
        *,
        graph_name: str,
        source_dataset: str,
        entities: list[EntityMetadata],
        relationships: list[RelationshipMetadata],
    ) -> GraphMetadata:

        graph = GraphMetadata(

            graph_name=graph_name,

            source_dataset=source_dataset,

            entities=entities,

            relationships=relationships,

        )

        # ------------------------------------------------
        # Group entities
        # ------------------------------------------------

        grouped = defaultdict(list)
        print("\n========== ENTITY DEBUG ==========")
        for entity in entities:
            print(entity.node_label, entity.label)
            print("Total Entities:", len(entities))

            print("==================================\n")

            grouped[entity.node_label].append(entity)

            # Use the entity label as the unique identifier
            graph.entities_by_identifier[
                (
                    entity.node_label,
                    entity.label,
                )
            ] = entity

        graph.entities_by_label = dict(grouped)

        # ------------------------------------------------
        # Statistics
        # ------------------------------------------------

        graph.node_count = len(entities)

        graph.edge_count = len(relationships)

        # ------------------------------------------------
        # Entity Types
        # ------------------------------------------------

        for entity in entities:

            graph.entity_types.setdefault(
                entity.node_label,
                0,
            )

            graph.entity_types[
                entity.node_label
            ] += 1

        # ------------------------------------------------
        # Relationship Types
        # ------------------------------------------------

        for relationship in relationships:

            graph.relationship_types.setdefault(
                relationship.relationship_type,
                0,
            )

            graph.relationship_types[
                relationship.relationship_type
            ] += 1

        return graph