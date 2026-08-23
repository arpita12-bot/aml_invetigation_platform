"""
==========================================================
AML Investigation Platform

Centrality Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CentralityResult:
    """
    Graph centrality metrics for an entity.
    """

    degree: float

    betweenness: float

    closeness: float

    pagerank: float

    graph_risk_score: float

    def to_dict(self) -> dict:

        return {

            "degree": self.degree,

            "betweenness": self.betweenness,

            "closeness": self.closeness,

            "pagerank": self.pagerank,

            "graph_risk_score": self.graph_risk_score,
        }