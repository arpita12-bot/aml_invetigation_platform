"""
==========================================================
AML Investigation Platform

Centrality Service

Responsibilities
----------------
✓ Retrieve graph centrality metrics
✓ Compute graph importance
✓ Produce graph risk score

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_analytics.centrality_result import (
    CentralityResult,
)


class CentralityService:
    """
    Reads graph centrality metrics from Neo4j.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    def analyze(
        self,
        entity_id: str,
    ) -> CentralityResult:

        query = """
        MATCH (n {entity_id:$entity_id})

        RETURN

        n.degree_centrality AS degree,

        n.betweenness_centrality AS betweenness,

        n.closeness_centrality AS closeness,

        n.page_rank AS pagerank
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                entity_id=entity_id,

            ).single()

        if record is None:

            return CentralityResult(

                degree=0.0,

                betweenness=0.0,

                closeness=0.0,

                pagerank=0.0,

                graph_risk_score=0.0,
            )

        score = self._calculate_graph_risk(

            degree=record["degree"],

            betweenness=record["betweenness"],

            closeness=record["closeness"],

            pagerank=record["pagerank"],
        )

        return CentralityResult(

            degree=record["degree"],

            betweenness=record["betweenness"],

            closeness=record["closeness"],

            pagerank=record["pagerank"],

            graph_risk_score=score,
        )

    @staticmethod
    def _calculate_graph_risk(
        *,
        degree: float,
        betweenness: float,
        closeness: float,
        pagerank: float,
    ) -> float:
        """
        Weighted graph importance score.

        All metrics are assumed normalized [0,100].
        """

        return round(

            degree * 0.25 +

            betweenness * 0.35 +

            closeness * 0.15 +

            pagerank * 0.25,

            2,
        )