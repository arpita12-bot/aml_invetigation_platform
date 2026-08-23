"""
==========================================================
AML Investigation Platform

Sanction Path Repository

Responsibilities
----------------
✓ Find shortest paths to sanctioned entities
✓ Calculate sanctions exposure
✓ Calculate sanctions risk
✓ Return structured sanction path results

==========================================================
"""

from __future__ import annotations

from typing import List

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.models.graph_gds.sanction_path_result import (
    SanctionPathResult,
)


class SanctionPathRepository:
    """
    Repository responsible for discovering
    graph paths between entities and sanctioned entities.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # =====================================================
    # Public Methods
    # =====================================================

    def find_sanction_paths(

        self,

        entity_id: str,

        max_depth: int = 6,

    ) -> List[SanctionPathResult]:

        query = """
        MATCH (source {entity_id:$entity_id})

        MATCH (sanction:Sanction)

        MATCH path = shortestPath(

            (source)-[*..$max_depth]-(sanction)

        )

        RETURN

            sanction.sanction_id AS sanction_id,

            sanction.name AS sanction_name,

            sanction.program AS sanction_program,

            sanction.jurisdiction AS jurisdiction,

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

                                        "sanction_id",

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

                    hop_count = int(

                        record["hop_count"]

                    )

                    paths.append(

                        SanctionPathResult(

                            source_entity_id=entity_id,

                            sanction_id=record["sanction_id"],

                            sanction_name=record["sanction_name"],

                            sanction_program=record["sanction_program"],

                            jurisdiction=record["jurisdiction"],

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

                "Failed to retrieve sanction paths."

            ) from exc

    # =====================================================
    # Private Helpers
    # =====================================================

    @staticmethod
    def _determine_exposure(

        hop_count: int,

    ) -> str:

        if hop_count == 1:

            return "DIRECT"

        if hop_count <= 3:

            return "INDIRECT"

        return "DISTANT"

    @staticmethod
    def _calculate_path_risk(

        hop_count: int,

    ) -> float:

        risk_matrix = {

            1: 1.00,

            2: 0.95,

            3: 0.85,

            4: 0.75,

            5: 0.65,

            6: 0.55,

        }

        return risk_matrix.get(hop_count, 0.45)