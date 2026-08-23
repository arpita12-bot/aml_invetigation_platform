"""
==========================================================
AML Investigation Platform

Centrality Repository

Responsibilities
----------------
✓ Execute Neo4j GDS centrality algorithms
✓ Persist centrality metrics
✓ Return number of updated nodes

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from neo4j.exceptions import Neo4jError


class CentralityRepository:

    """
    Repository responsible for executing
    Neo4j Graph Data Science centrality algorithms.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # ---------------------------------------------------
    # Public Algorithms
    # ---------------------------------------------------

    def run_degree(
        self,
        graph_name: str,
    ) -> int:

        return self._execute_algorithm(

            procedure="gds.degree.write",

            graph_name=graph_name,

            property_name="degree_centrality",
        )

    def run_betweenness(
        self,
        graph_name: str,
    ) -> int:

        return self._execute_algorithm(

            procedure="gds.betweenness.write",

            graph_name=graph_name,

            property_name="betweenness_centrality",
        )

    def run_closeness(
        self,
        graph_name: str,
    ) -> int:

        return self._execute_algorithm(

            procedure="gds.closeness.write",

            graph_name=graph_name,

            property_name="closeness_centrality",
        )

    def run_pagerank(
        self,
        graph_name: str,
    ) -> int:

        return self._execute_algorithm(

            procedure="gds.pageRank.write",

            graph_name=graph_name,

            property_name="page_rank",
        )

    # ---------------------------------------------------
    # Internal Helper
    # ---------------------------------------------------

    def _execute_algorithm(
        self,
        *,
        procedure: str,
        graph_name: str,
        property_name: str,
    ) -> int:

        query = f"""
        CALL {procedure}(

            $graph_name,

            {{

                writeProperty:$property_name

            }}

        )

        YIELD nodePropertiesWritten
        """

        try:

            with self._driver.session() as session:

                record = session.run(

                    query,

                    graph_name=graph_name,

                    property_name=property_name,

                ).single()

            if record is None:

                return 0

            return int(record["nodePropertiesWritten"])

        except Neo4jError as exc:

            raise RuntimeError(

                f"{procedure} failed."

            ) from exc