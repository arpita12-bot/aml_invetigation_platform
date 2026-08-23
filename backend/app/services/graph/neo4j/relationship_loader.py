"""
==========================================================
AML Investigation Platform

Neo4j Relationship Loader

Responsibilities
----------------
✓ Batch relationship loading
✓ Dynamic relationship types
✓ UNWIND loading
✓ Transaction friendly

==========================================================
"""

from __future__ import annotations

from collections import defaultdict

from app.models.graph.graph_metadata import GraphMetadata
from app.services.graph.neo4j.batch_manager import BatchManager
from app.services.graph.neo4j.cypher_builder import CypherBuilder


class RelationshipLoader:

    @classmethod
    def load(
        cls,
        *,
        session,
        graph: GraphMetadata,
        batch_size: int = 5000,
    ) -> int:

        grouped_relationships = defaultdict(list)

        # ----------------------------------------
        # Group relationships by type
        # ----------------------------------------

        for relationship in graph.relationships:

            grouped_relationships[
                relationship.relationship_type
            ].append(relationship)

        total_loaded = 0

        # ----------------------------------------
        # Process each relationship type
        # ----------------------------------------

        for relationship_type, relationships in grouped_relationships.items():

            if not relationships:
                continue

            first = relationships[0]

            cypher = CypherBuilder.merge_relationships(

                source_label=first.source_label,

                target_label=first.target_label,

                relationship_type=relationship_type,

                source_identifier=first.source_identifier,

                target_identifier=first.target_identifier,

            )

            rows = []

            for relationship in relationships:

                rows.append({

                    "source_id":
                        relationship.source_identifier_value,

                    "target_id":
                        relationship.target_identifier_value,

                    "properties":
                        relationship.properties,

                })

            for batch in BatchManager.batches(

                rows,

                batch_size,

            ):

                session.run(

                    cypher,

                    rows=batch,

                )

                total_loaded += len(batch)

        return total_loaded