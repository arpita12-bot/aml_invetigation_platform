"""
==========================================================
AML Investigation Platform

Graph Metrics Result

Represents global statistics for the Knowledge Graph.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GraphMetricsResult:
    """
    Global graph statistics.
    """

    node_count: int = 0

    relationship_count: int = 0

    density: float = 0.0

    average_degree: float = 0.0

    clustering_coefficient: float = 0.0

    average_path_length: float = 0.0

    graph_diameter: int = 0

    connected_components: int = 0

    largest_component_size: int = 0

    modularity: float = 0.0

    def to_dict(self) -> dict:

        return {

            "node_count": self.node_count,

            "relationship_count": self.relationship_count,

            "density": self.density,

            "average_degree": self.average_degree,

            "clustering_coefficient":
                self.clustering_coefficient,

            "average_path_length":
                self.average_path_length,

            "graph_diameter":
                self.graph_diameter,

            "connected_components":
                self.connected_components,

            "largest_component_size":
                self.largest_component_size,

            "modularity":
                self.modularity,
        }