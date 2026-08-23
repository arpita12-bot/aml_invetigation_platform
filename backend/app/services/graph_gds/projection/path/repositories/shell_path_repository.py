"""
==========================================================
AML Investigation Platform

Shell Path Repository

Responsibilities
----------------
✓ Discover shell company structures
✓ Combine graph intelligence
✓ Calculate shell suspicion score

==========================================================
"""

from __future__ import annotations

from typing import List

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.models.graph_gds.shell_path_result import (
    ShellPathResult,
)


class ShellPathRepository:

    def __init__(
        self,
        driver: Driver,
    ):
        self._driver = driver

    # =====================================================
    # Public Methods
    # =====================================================

    def find_shell_company_paths(
        self,
        entity_id: str,
        max_depth: int = 6,
    ) -> List[ShellPathResult]:

        query = """
        MATCH (source {entity_id:$entity_id})

        MATCH (shell:Company)

        WHERE shell.is_shell_company = true

        MATCH path = shortestPath(

            (source)-[:OWNS|DIRECTOR_OF|SHAREHOLDER_OF*..$max_depth]->(shell)

        )

        RETURN

            shell.company_id AS company_id,

            shell.name AS company_name,

            shell.community_id AS community_id,

            shell.page_rank AS page_rank,

            shell.similarity_score AS similarity_score,

            shell.link_prediction_score AS link_prediction_score,

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

                shell_paths = []

                for record in result:

                    ownership_chain = [

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

                    hop_count = int(record["hop_count"])

                    similarity = float(
                        record.get(
                            "similarity_score",
                            0.0,
                        )
                    )

                    pagerank = float(
                        record.get(
                            "page_rank",
                            0.0,
                        )
                    )

                    prediction = float(
                        record.get(
                            "link_prediction_score",
                            0.0,
                        )
                    )

                    suspicion = self._calculate_suspicion_score(

                        hop_count,

                        similarity,

                        pagerank,

                        prediction,

                    )

                    shell_paths.append(

                        ShellPathResult(

                            source_entity_id=entity_id,

                            shell_company_id=record["company_id"],

                            shell_company_name=record["company_name"],

                            hop_count=hop_count,

                            ownership_chain=ownership_chain,

                            relationship_chain=relationship_chain,

                            community_id=record["community_id"],

                            similarity_score=similarity,

                            page_rank=pagerank,

                            link_prediction_score=prediction,

                            suspicion_score=suspicion,

                            explanation=self._generate_explanation(
                                hop_count,
                                suspicion,
                            ),
                        )

                    )

                return shell_paths

        except Neo4jError as exc:

            raise RuntimeError(

                "Failed to discover shell company paths."

            ) from exc

    # =====================================================
    # Private Helpers
    # =====================================================

    @staticmethod
    def _calculate_suspicion_score(
        hop_count: int,
        similarity: float,
        pagerank: float,
        prediction: float,
    ) -> float:

        hop_component = min(hop_count / 6, 1.0)

        score = (

            hop_component * 0.25 +

            similarity * 0.25 +

            pagerank * 0.20 +

            prediction * 0.30

        )

        return round(score, 3)

    @staticmethod
    def _generate_explanation(
        hop_count: int,
        suspicion_score: float,
    ) -> str:

        if suspicion_score >= 0.90:

            return (
                "Very high shell company suspicion "
                "based on ownership chain and graph analytics."
            )

        if suspicion_score >= 0.75:

            return (
                "High shell company suspicion requiring "
                "manual investigation."
            )

        if suspicion_score >= 0.60:

            return (
                "Moderate shell company risk."
            )

        return (
            "Low shell company suspicion."
        )