"""
==========================================================
AML Investigation Platform

Centrality Reader Repository

Responsibilities
----------------
✓ Read persisted graph centrality metrics
✓ Retrieve metrics for investigations
✓ Retrieve top ranked entities

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_gds.centrality_metrics import (
    CentralityMetrics,
)


class CentralityReaderRepository:

    """
    Reads persisted GDS metrics from Neo4j.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def find_customer_metrics(
        self,
        customer_id: str,
    ) -> list[CentralityMetrics]:

        return self.find_entity_metrics(
            entity_id=customer_id,
            label="Customer",
        )

    def find_account_metrics(
        self,
        account_id: str,
    ) -> list[CentralityMetrics]:

        return self.find_entity_metrics(
            entity_id=account_id,
            label="Account",
        )

    def find_company_metrics(
        self,
        company_id: str,
    ) -> list[CentralityMetrics]:

        return self.find_entity_metrics(
            entity_id=company_id,
            label="Company",
        )

    def find_entity_metrics(
        self,
        entity_id: str,
        label: str,
    ) -> list[CentralityMetrics]:

        query = f"""
        MATCH (n:{label})

        WHERE n.id = $entity_id

        RETURN

            n.id AS entity_id,

            labels(n)[0] AS label,

            coalesce(n.page_rank,0.0) AS page_rank,

            coalesce(n.degree_centrality,0.0) AS degree_centrality,

            coalesce(n.betweenness_centrality,0.0) AS betweenness_centrality,

            coalesce(n.closeness_centrality,0.0) AS closeness_centrality
        """

        with self._driver.session() as session:

            result = session.run(
                query,
                entity_id=entity_id,
            )

            return [

                CentralityMetrics(

                    entity_id=row["entity_id"],

                    label=row["label"],

                    page_rank=row["page_rank"],

                    degree_centrality=row["degree_centrality"],

                    betweenness_centrality=row["betweenness_centrality"],

                    closeness_centrality=row["closeness_centrality"],

                )

                for row in result

            ]

    def top_central_nodes(
        self,
        *,
        label: str,
        limit: int = 25,
    ) -> list[CentralityMetrics]:

        query = f"""
        MATCH (n:{label})

        RETURN

            n.id AS entity_id,

            labels(n)[0] AS label,

            coalesce(n.page_rank,0.0) AS page_rank,

            coalesce(n.degree_centrality,0.0) AS degree_centrality,

            coalesce(n.betweenness_centrality,0.0) AS betweenness_centrality,

            coalesce(n.closeness_centrality,0.0) AS closeness_centrality

        ORDER BY page_rank DESC

        LIMIT $limit
        """

        with self._driver.session() as session:

            result = session.run(
                query,
                limit=limit,
            )

            return [

                CentralityMetrics(

                    entity_id=row["entity_id"],

                    label=row["label"],

                    page_rank=row["page_rank"],

                    degree_centrality=row["degree_centrality"],

                    betweenness_centrality=row["betweenness_centrality"],

                    closeness_centrality=row["closeness_centrality"],

                )

                for row in result

            ]