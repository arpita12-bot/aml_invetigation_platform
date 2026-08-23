"""
==========================================================
AML Investigation Platform

Foreign Key Relationship Provider

Responsibilities
----------------
✓ Discover relationships from foreign keys
✓ Convert FK metadata to RelationshipMetadata
✓ Use cached metadata only
✓ No direct database queries

==========================================================
"""

from __future__ import annotations

from typing import List

from app.models.schema.relationship_metadata import RelationshipMetadata
from app.services.graph.discovery.metadata_cache import MetadataCache


class ForeignKeyProvider:
    """
    Discovers relationships using cached foreign key metadata.
    """

    def discover(
        self,
        cache: MetadataCache,
    ) -> List[RelationshipMetadata]:

        relationships: List[RelationshipMetadata] = []

        for source_table, foreign_keys in cache.foreign_keys.items():

            source_graph = cache.graph(source_table)

            if source_graph is None:
                continue

            for fk in foreign_keys:

                target_table = fk["target_table"]

                target_graph = cache.graph(target_table)

                if target_graph is None:
                    continue

                relationship_name = (
                    f"{source_graph.node_label.upper()}_TO_"
                    f"{target_graph.node_label.upper()}"
                )

                relationships.append(

                    RelationshipMetadata(

                        source_table=source_table,
                        source_column=fk["source_column"],
                        source_entity=source_graph.node_label,

                        target_table=target_table,
                        target_column=fk["target_column"],
                        target_entity=target_graph.node_label,

                        relationship_name=relationship_name,
                        relationship_type=relationship_name,

                        source_label=source_graph.node_label,
                        source_identifier=source_graph.identifier_column,

                        target_label=target_graph.node_label,
                        target_identifier=target_graph.identifier_column,

                        inferred=False,

                        confidence=1.0,

                        neo4j_relationship=relationship_name,
                    )

                )

        return relationships