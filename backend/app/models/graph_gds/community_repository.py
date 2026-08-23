"""
Repository for Neo4j GDS Community Detection.
"""

from neo4j import Driver

import time
from app.models.graph_gds.community_job_result import (
    CommunityJobResult,
)

from app.models.graph_gds.community_statistics_result import (
    CommunityStatisticsResult,
)

class CommunityRepository:

    def __init__(self, driver: Driver):

        self._driver = driver

    def run_louvain(
        self,
        graph_name: str,
    ) -> CommunityJobResult:

        query = """
        CALL gds.louvain.write(

            $graph_name,

            {

                writeProperty:'community_id'

            }

        )

        YIELD

            communityCount,

            modularity,

            nodePropertiesWritten,

            computeMillis
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                graph_name=graph_name,

            ).single()

        return CommunityJobResult(

            graph_name=graph_name,

            communities_found=record["communityCount"],

            modularity=record["modularity"],

            node_properties_written=record[
                "nodePropertiesWritten"
            ],

            execution_time_seconds=
                record["computeMillis"] / 1000,

            successful=True,
        )
        
    # -----------------------------------------------------
    # Community Statistics
    # -----------------------------------------------------

    def calculate_community_statistics(
        self,
    ) -> CommunityStatisticsResult:
        """
        Calculate and persist community-level statistics after
        Louvain community detection.

        Populates:
        - community_size
        - suspicious_entities
        - community_risk
        """

        start_time = time.perf_counter()

        query = """
        MATCH (n)
        WHERE n.community_id IS NOT NULL

        WITH
            n.community_id AS community,
            collect(n) AS members,
            count(*) AS communitySize,
            sum(
                CASE
                    WHEN coalesce(n.risk_level, '') IN ['HIGH', 'CRITICAL']
                    THEN 1
                    ELSE 0
                END
            ) AS suspiciousEntities

        UNWIND members AS node

        SET
            node.community_size = communitySize,
            node.suspicious_entities = suspiciousEntities,
            node.community_risk =
                CASE
                    WHEN communitySize = 0 THEN 0.0
                    ELSE round((100.0 * suspiciousEntities) / communitySize, 2)
                END

        RETURN
            count(node) AS updatedNodes,
            count(DISTINCT community) AS communitiesProcessed
        """

        with self._driver.session() as session:

            record = session.run(query).single()

        execution_time = time.perf_counter() - start_time

        return CommunityStatisticsResult(

            communities_processed=(
                record["communitiesProcessed"]
                if record else 0
            ),

            nodes_updated=(
                record["updatedNodes"]
                if record else 0
            ),

            execution_time_seconds=round(
                execution_time,
                3,
            ),

            successful=True,
        )