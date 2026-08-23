"""
==========================================================
AML Investigation Platform

Graph Metrics Service

Responsibilities
----------------
✓ Retrieve graph statistics
✓ Compute global graph metrics
✓ Provide graph health indicators

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_analytics.graph_metrics_result import (
    GraphMetricsResult,
)


class GraphMetricsService:
    """
    Retrieves graph-wide metrics from Neo4j.
    """

    def __init__(self, driver: Driver):

        self._driver = driver

    def analyze(self) -> GraphMetricsResult:

        query = """
        MATCH (n)

        OPTIONAL MATCH ()-[r]->()

        RETURN

            count(DISTINCT n) AS node_count,

            count(DISTINCT r) AS relationship_count
        """

        with self._driver.session() as session:

            record = session.run(query).single()

        if record is None:

            return GraphMetricsResult()

        node_count = record["node_count"]

        relationship_count = record["relationship_count"]

        density = self._calculate_density(

            node_count,

            relationship_count,
        )

        average_degree = self._calculate_average_degree(

            node_count,

            relationship_count,
        )

        return GraphMetricsResult(

            node_count=node_count,

            relationship_count=relationship_count,

            density=density,

            average_degree=average_degree,

            clustering_coefficient=0.0,

            average_path_length=0.0,

            graph_diameter=0,

            connected_components=0,

            largest_component_size=0,

            modularity=0.0,
        )

    @staticmethod
    def _calculate_density(
        nodes: int,
        relationships: int,
    ) -> float:

        if nodes <= 1:

            return 0.0

        max_edges = nodes * (nodes - 1)

        return round(

            relationships / max_edges,

            6,
        )

    @staticmethod
    def _calculate_average_degree(
        nodes: int,
        relationships: int,
    ) -> float:

        if nodes == 0:

            return 0.0

        return round(

            (2 * relationships) / nodes,

            2,
        )