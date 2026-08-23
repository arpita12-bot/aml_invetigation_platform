"""
==========================================================
AML Investigation Platform

Ownership Path Repository

Responsibilities
----------------
✓ Discover ownership chains
✓ Find indirect ownership
✓ Find beneficial ownership
✓ Return structured ownership paths

==========================================================
"""

from __future__ import annotations

from typing import List

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.models.graph_gds.ownership_path_result import (
    OwnershipPathResult,
)


class OwnershipPathRepository:

    """
    Repository responsible for ownership path discovery.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # =========================================================
    # Public Methods
    # =========================================================

    def find_ownership_paths(

        self,

        entity_id: str,

        max_depth: int = 6,

    ) -> List[OwnershipPathResult]:

        query = """
        MATCH (source {entity_id:$entity_id})

        MATCH (company:Company)

        MATCH path = shortestPath(

            (source)-[:OWNS|DIRECTOR_OF|SHAREHOLDER_OF*..$max_depth]->(company)

        )

        RETURN

            company.company_id AS company_id,

            company.name AS company_name,

            company.ownership_percentage AS ownership_percentage,

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

                ownership_paths = []

                for record in result:

                    node_chain = [

                        node.get(

                            "entity_id",

                            node.get(

                                "company_id",

                                str(node.id)

                            )

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

                    ownership_paths.append(

                        OwnershipPathResult(

                            source_entity_id=entity_id,

                            target_company_id=record["company_id"],

                            target_company_name=record["company_name"],

                            ownership_percentage=float(

                                record.get(

                                    "ownership_percentage",

                                    0.0,

                                )

                            ),

                            hop_count=hop_count,

                            relationship_chain=relationship_chain,

                            node_chain=node_chain,

                            ownership_type=self._determine_ownership_type(

                                hop_count

                            ),

                            path_risk_score=self._calculate_path_risk(

                                hop_count

                            ),
                        )

                    )

                return ownership_paths

        except Neo4jError as exc:

            raise RuntimeError(

                "Failed to retrieve ownership paths."

            ) from exc

    # =========================================================
    # Private Helpers
    # =========================================================

    @staticmethod
    def _determine_ownership_type(

        hop_count: int,

    ) -> str:

        if hop_count == 1:

            return "DIRECT"

        if hop_count <= 3:

            return "INDIRECT"

        return "BENEFICIAL"

    @staticmethod
    def _calculate_path_risk(

        hop_count: int,

    ) -> float:

        risk_matrix = {

            1: 0.40,

            2: 0.60,

            3: 0.75,

            4: 0.85,

            5: 0.95,

            6: 1.00,

        }

        return risk_matrix.get(hop_count, 1.00)