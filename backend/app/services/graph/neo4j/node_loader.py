"""
==========================================================
AML Investigation Platform

Neo4j Node Loader

Responsibilities
----------------
✓ Batch loading
✓ UNWIND loading
✓ Transaction friendly

==========================================================
"""

from __future__ import annotations

from app.models.graph.graph_metadata import GraphMetadata
from app.services.graph.neo4j.batch_manager import BatchManager
from app.services.graph.neo4j.cypher_builder import CypherBuilder


class NodeLoader:

    @classmethod
    def load(
        cls,
        *,
        session,
        graph: GraphMetadata,
        batch_size: int = 5000,
    ) -> int:

        total_loaded = 0

        for label, entities in graph.entities_by_label.items():

            if not entities:
                continue

            #
            # We now use "label" as the unique identifier
            #
            identifier_property = "label"

            cypher = CypherBuilder.merge_nodes(
                label=label,
                identifier_property=identifier_property,
            )

            rows = []

            for entity in entities:

                row = dict(entity.properties)

                #
                # Standard graph properties
                #
                row["label"] = entity.label
                row["entity_type"] = entity.entity_type
                row["source_table"] = entity.source_table
                row["source_column"] = entity.source_column
                row["confidence"] = entity.confidence

                rows.append(row)

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