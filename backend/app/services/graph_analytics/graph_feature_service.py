"""
==========================================================
AML Investigation Platform

Graph Feature Service

Responsibilities
----------------
✓ Aggregate graph analytics
✓ Build GraphFeatures
✓ Hide graph implementation details

==========================================================
"""

from __future__ import annotations

from app.models.graph_analytics.graph_features import (
    GraphFeatures,
)

from app.models.graph_analytics.community.community_detection_service import (
    CommunityDetectionService,
)

from app.services.graph_analytics.centrality.centrality_service import (
    CentralityService,
)

from app.services.graph_analytics.path.path_analysis_service import (
    PathAnalysisService,
)

from app.models.graph_analytics.patterns.shell_pattern_service import (
    ShellPatternService,
)

from app.services.graph_analytics.metrics.graph_metrics_service import (
    GraphMetricsService,
)


class GraphFeatureService:
    """
    Main orchestration service for graph analytics.
    """

    def __init__(
        self,
        community_service: CommunityDetectionService,
        centrality_service: CentralityService,
        path_service: PathAnalysisService,
        shell_pattern_service: ShellPatternService,
        graph_metrics_service: GraphMetricsService,
    ):

        self._community_service = community_service

        self._centrality_service = centrality_service

        self._path_service = path_service

        self._shell_pattern_service = shell_pattern_service

        self._graph_metrics_service = graph_metrics_service

    def extract(
        self,
        entity_id: str,
    ) -> GraphFeatures:
        """
        Build GraphFeatures for a single entity.
        """

        community = self._community_service.detect(
            entity_id
        )

        centrality = self._centrality_service.analyze(
            entity_id
        )

        paths = self._path_service.analyze(
            entity_id
        )

        shell = self._shell_pattern_service.analyze(
            entity_id
        )

        graph_metrics = self._graph_metrics_service.analyze()

        graph_risk = self._calculate_graph_risk(

            community.risk_score,

            centrality.graph_risk_score,

            paths.graph_risk_score,

            shell.shell_pattern_score,
        )

        return GraphFeatures(

            degree_centrality=centrality.degree,

            betweenness_centrality=centrality.betweenness,

            closeness_centrality=centrality.closeness,

            pagerank=centrality.pagerank,

            community_id=community.community_id,

            community_score=community.risk_score,

            shortest_path_to_pep=(
                paths.shortest_path_to_pep.length
                if paths.shortest_path_to_pep
                else None
            ),

            shortest_path_to_sanction=(
                paths.shortest_path_to_sanction.length
                if paths.shortest_path_to_sanction
                else None
            ),

            circular_transaction_count=(
                shell.circular_transaction_count
            ),

            shared_directors=shell.shared_directors,

            shared_addresses=shell.shared_addresses,

            shared_phone_numbers=shell.shared_phone_numbers,

            shared_devices=shell.shared_devices,

            shell_pattern_score=(
                shell.shell_pattern_score
            ),

            graph_risk_score=graph_risk,

            warnings=[],
        )

    @staticmethod
    def _calculate_graph_risk(
        community_score: float,
        centrality_score: float,
        path_score: float,
        shell_score: float,
    ) -> float:
        """
        Aggregate graph intelligence into
        one normalized score.
        """

        score = (

            community_score * 0.25 +

            centrality_score * 0.30 +

            path_score * 0.20 +

            shell_score * 0.25

        )

        return round(min(score, 100), 2)