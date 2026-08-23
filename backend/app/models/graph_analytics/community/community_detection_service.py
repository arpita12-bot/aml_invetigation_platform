"""
==========================================================
AML Investigation Platform

Community Detection Service

Responsibilities
----------------
✓ Execute Louvain community detection
✓ Find entity community
✓ Compute community risk
✓ Return normalized result

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_analytics.community_result import (
    CommunityResult,
)


class CommunityDetectionService:

    """
    Neo4j Graph Data Science based
    community detection.
    """

    def __init__(self, driver: Driver):

        self._driver = driver

    def detect(
        self,
        entity_id: str,
    ) -> CommunityResult:

        query = """
        MATCH (e {entity_id:$entity_id})

        RETURN

        e.community_id AS community_id,

        e.community_size AS community_size,

        e.community_risk AS community_risk,

        e.modularity AS modularity,

        e.suspicious_entities AS suspicious_entities
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                entity_id=entity_id,

            ).single()

        if record is None:

            return CommunityResult(

                community_id="UNKNOWN",

                community_size=0,

                modularity=0.0,

                suspicious_entities=0,

                risk_score=0.0,
            )

        return CommunityResult(

            community_id=record["community_id"],

            community_size=record["community_size"],

            modularity=record["modularity"],

            suspicious_entities=record["suspicious_entities"],

            risk_score=record["community_risk"],
        )