"""
==========================================================
AML Investigation Platform

Graph Features

Represents graph-derived intelligence computed
from the Knowledge Graph.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphFeatures:
    """
    Graph-derived AML features.

    All numeric scores are normalized to [0,100].
    """

    # --------------------------------------------
    # Connectivity
    # --------------------------------------------

    degree_centrality: float = 0.0

    betweenness_centrality: float = 0.0

    closeness_centrality: float = 0.0

    pagerank: float = 0.0

    # --------------------------------------------
    # Community
    # --------------------------------------------

    community_id: str | None = None

    community_score: float = 0.0

    # --------------------------------------------
    # Graph Structure
    # --------------------------------------------

    shortest_path_to_pep: int | None = None

    shortest_path_to_sanction: int | None = None

    circular_transaction_count: int = 0

    # --------------------------------------------
    # Shared Identity
    # --------------------------------------------

    shared_directors: int = 0

    shared_addresses: int = 0

    shared_phone_numbers: int = 0

    shared_devices: int = 0

    # --------------------------------------------
    # Shell Indicators
    # --------------------------------------------

    shell_pattern_score: float = 0.0

    # --------------------------------------------
    # Graph Risk
    # --------------------------------------------

    graph_risk_score: float = 0.0

    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:

        return {

            "degree_centrality": self.degree_centrality,

            "betweenness_centrality": self.betweenness_centrality,

            "closeness_centrality": self.closeness_centrality,

            "pagerank": self.pagerank,

            "community_id": self.community_id,

            "community_score": self.community_score,

            "shortest_path_to_pep": self.shortest_path_to_pep,

            "shortest_path_to_sanction": self.shortest_path_to_sanction,

            "circular_transaction_count": self.circular_transaction_count,

            "shared_directors": self.shared_directors,

            "shared_addresses": self.shared_addresses,

            "shared_phone_numbers": self.shared_phone_numbers,

            "shared_devices": self.shared_devices,

            "shell_pattern_score": self.shell_pattern_score,

            "graph_risk_score": self.graph_risk_score,

            "warnings": self.warnings,
        }