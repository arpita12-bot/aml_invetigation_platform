"""
==========================================================
AML Investigation Platform

Path Analysis Service

Responsibilities
----------------
✓ Find shortest paths
✓ Discover ownership chains
✓ Detect circular transaction paths
✓ Calculate path-based graph risk

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_analytics.path_analysis_result import (
    PathAnalysisResult,
)


class PathAnalysisService:

    """
    Performs graph traversal analysis
    using Neo4j.
    """

    def __init__(self, driver: Driver):

        self._driver = driver

    def analyze(
        self,
        entity_id: str,
    ) -> PathAnalysisResult:

        #
        # This version intentionally acts as an
        # orchestration layer.
        #
        # Each helper performs one analysis.
        #

        pep_path = self._find_pep_path(entity_id)

        sanction_path = self._find_sanction_path(entity_id)

        ownership_chain = self._find_ownership_chain(entity_id)

        circular_paths = self._find_circular_paths(entity_id)

        graph_score = self._calculate_graph_score(

            pep_path,

            sanction_path,

            circular_paths,
        )

        return PathAnalysisResult(

            shortest_path_to_pep=pep_path,

            shortest_path_to_sanction=sanction_path,

            ownership_chain=ownership_chain,

            circular_paths=circular_paths,

            total_paths=len(circular_paths),

            graph_risk_score=graph_score,
        )

    #
    # Private methods
    #

    def _find_pep_path(self, entity_id):
        raise NotImplementedError

    def _find_sanction_path(self, entity_id):
        raise NotImplementedError

    def _find_ownership_chain(self, entity_id):
        raise NotImplementedError

    def _find_circular_paths(self, entity_id):
        raise NotImplementedError

    @staticmethod
    def _calculate_graph_score(
        pep_path,
        sanction_path,
        circular_paths,
    ) -> float:

        score = 0.0

        if pep_path:
            score += 25

        if sanction_path:
            score += 40

        score += min(len(circular_paths) * 10, 35)

        return min(score, 100)