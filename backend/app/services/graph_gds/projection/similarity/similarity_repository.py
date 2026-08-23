"""
==========================================================
AML Investigation Platform

Similarity Repository

==========================================================
"""

from __future__ import annotations

from neo4j import Driver
from neo4j.exceptions import Neo4jError


class SimilarityRepository:

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    def run_node_similarity(
        self,
        graph_name: str,
        similarity_threshold: float,
        top_k: int,
    ) -> tuple[int, int]:

        query = """
        CALL gds.nodeSimilarity.write(

            $graph_name,

            {

                writeRelationshipType:'SIMILAR_TO',

                writeProperty:'score',

                similarityCutoff:$threshold,

                topK:$top_k

            }

        )

        YIELD

            nodesCompared,

            relationshipsWritten
        """

        try:

            with self._driver.session() as session:

                record = session.run(

                    query,

                    graph_name=graph_name,

                    threshold=similarity_threshold,

                    top_k=top_k,

                ).single()

            if record is None:

                return 0, 0

            return (

                int(record["relationshipsWritten"]),

                int(record["nodesCompared"]),
            )

        except Neo4jError as exc:

            raise RuntimeError(
                "Node Similarity execution failed."
            ) from exc