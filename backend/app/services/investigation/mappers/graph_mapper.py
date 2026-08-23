"""
==========================================================
AML Investigation Platform

Graph Mapper

Responsibilities
----------------
✓ Convert InvestigationGraph
✓ Convert GraphNode
✓ Convert GraphRelationship

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.graph_node_dto import (
    GraphNodeDTO,
)

from app.api.investigation.schemas.graph_relationship_dto import (
    GraphRelationshipDTO,
)

from app.models.investigation.investigation_graph import (
    InvestigationGraph,
)


class GraphMapper:
    """
    Maps InvestigationGraph into API DTOs.
    """

    @staticmethod
    def map_nodes(
        graph: InvestigationGraph,
    ) -> list[GraphNodeDTO]:

        return [

            GraphNodeDTO(

                node_id=node.node_id,

                label=node.label,

                properties=node.properties,

            )

            for node in graph.nodes

        ]

    @staticmethod
    def map_relationships(
        graph: InvestigationGraph,
    ) -> list[GraphRelationshipDTO]:

        return [

            GraphRelationshipDTO(

                relationship_type=
                    relationship.relationship_type,

                source_id=
                    relationship.source_id,

                target_id=
                    relationship.target_id,

                properties=
                    relationship.properties,

            )

            for relationship in graph.relationships

        ]