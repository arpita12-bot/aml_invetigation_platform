"""
==========================================================
AML Investigation Platform

Graph Metadata

Represents metadata required to construct
the Knowledge Graph.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.schema.relationship_metadata import (
    RelationshipMetadata,
)


@dataclass(slots=True)
class GraphMetadata:
    """
    Metadata describing the graph.
    """

    graph_name: str

    node_labels: list[str] = field(
        default_factory=list
    )

    relationship_labels: list[str] = field(
        default_factory=list
    )

    relationships: list[
        RelationshipMetadata
    ] = field(default_factory=list)

    node_count: int = 0

    relationship_count: int = 0

    directed: bool = True

    weighted: bool = False

    properties: dict = field(
        default_factory=dict
    )

    def add_relationship(
        self,
        relationship: RelationshipMetadata,
    ) -> None:

        self.relationships.append(
            relationship
        )

        self.relationship_count = len(
            self.relationships
        )

    def to_dict(self):

        return {

            "graph_name": self.graph_name,

            "node_labels": self.node_labels,

            "relationship_labels": self.relationship_labels,

            "node_count": self.node_count,

            "relationship_count": self.relationship_count,

            "directed": self.directed,

            "weighted": self.weighted,

            "properties": self.properties,

            "relationships": [

                relationship.to_dict()

                for relationship in self.relationships

            ],

        }