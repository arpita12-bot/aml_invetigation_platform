"""
==========================================================
AML Investigation Platform

Graph Projection Model

Represents a Neo4j GDS projected graph.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GraphProjection:

    graph_name: str

    node_count: int

    relationship_count: int

    node_labels: list[str]

    relationship_types: list[str]

    exists: bool

    def to_dict(self) -> dict:

        return {

            "graph_name": self.graph_name,

            "node_count": self.node_count,

            "relationship_count": self.relationship_count,

            "node_labels": self.node_labels,

            "relationship_types": self.relationship_types,

            "exists": self.exists,
        }