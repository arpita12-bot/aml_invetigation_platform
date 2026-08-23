"""
==========================================================
AML Investigation Platform

Centrality Metrics

Responsibilities
----------------
✓ Represent persisted GDS centrality metrics
✓ Used during investigation evidence collection

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CentralityMetrics:
    """
    Persisted graph centrality metrics for a node.
    """

    entity_id: str

    label: str

    page_rank: float = 0.0

    degree_centrality: float = 0.0

    betweenness_centrality: float = 0.0

    closeness_centrality: float = 0.0