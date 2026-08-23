"""
==========================================================
AML Investigation Platform

PEP Path Repository

Responsibilities
----------------
✓ Find shortest paths to Politically Exposed Persons (PEPs)
✓ Calculate PEP exposure level
✓ Calculate path risk score
✓ Return structured PEP path results

==========================================================
"""

from __future__ import annotations

from typing import List

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.models.graph_gds.pep_path_result import PepPathResult


class PepPathRepository:
    """
    Repository responsible for discovering
    paths between entities and PEPs.
    """

    def __init__(
        self,
        driver: Driver,
    ):
        self._driver = driver

    # ==========================================================
    # Public Methods
    # ==========================================================

    def find_pep_paths(
        self,
        entity_id: str,
        max_depth: int = 6,
    ) -> List[PepPathResult]:
        """
        Find all shortest paths from an entity
        to Politically Exposed Persons.
        """

        query = """
        MATCH (source {entity_id:$entity_id})

        MATCH (pep:PEP)

        MATCH path = shortestPath(

            (source)-[*..$max_depth]-(pep)

        )

        RETURN

            pep.pep_id AS pep_id,

            pep.name AS pep_name,

            length(path) AS hop_count,

            nodes(path) AS nodes,

            relationships(path) AS relationships
        """

        try:

            with self._driver.session() as session:

                result = session.run(
                    query,
                    entity_id=entity_id,
                    max_depth=max_depth,
                )

                paths = []

                for record in result:

                    node_chain = [
                        node.get(
                            "entity_id",
                            node.get(
                                "customer_id",
                                node.get(
                                    "company_id",
                                    node.get(
                                        "pep_id",
                                        str(node.id),
                                    ),
                                ),
                            ),
                        )
                        for node in record["nodes"]
                    ]

                    relationship_chain = [
                        relationship.type
                        for relationship in record["relationships"]
                    ]

                    hop_count = int(record["hop_count"])

                    paths.append(

                        PepPathResult(

                            source_entity_id=entity_id,

                            pep_id=record["pep_id"],

                            pep_name=record["pep_name"],

                            hop_count=hop_count,

                            relationship_chain=relationship_chain,

                            node_chain=node_chain,

                            exposure_level=self._determine_exposure(
                                hop_count
                            ),

                            path_risk_score=self._calculate_path_risk(
                                hop_count
                            ),
                        )

                    )

                return paths

        except Neo4jError as exc:

            raise RuntimeError(
                "Failed to retrieve PEP paths."
            ) from exc

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _determine_exposure(
        hop_count: int,
    ) -> str:
        """
        Determine exposure level based on hop count.
        """

        if hop_count == 1:
            return "DIRECT"

        if hop_count <= 3:
            return "INDIRECT"

        return "DISTANT"

    @staticmethod
    def _calculate_path_risk(
        hop_count: int,
    ) -> float:
        """
        Calculate path risk score.
        """

        risk_matrix = {

            1: 1.00,

            2: 0.90,

            3: 0.80,

            4: 0.70,

            5: 0.60,

            6: 0.50,

        }

        return risk_matrix.get(hop_count, 0.40)