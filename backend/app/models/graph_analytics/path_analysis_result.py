"""
==========================================================
AML Investigation Platform

Path Analysis Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.graph_analytics.graph_path import (
    GraphPath,
)


@dataclass(slots=True)
class PathAnalysisResult:

    shortest_path_to_pep: GraphPath | None = None

    shortest_path_to_sanction: GraphPath | None = None

    ownership_chain: GraphPath | None = None

    circular_paths: list[GraphPath] = field(default_factory=list)

    total_paths: int = 0

    graph_risk_score: float = 0.0

    def to_dict(self):

        return {

            "shortest_path_to_pep":
                None if self.shortest_path_to_pep is None
                else self.shortest_path_to_pep.to_dict(),

            "shortest_path_to_sanction":
                None if self.shortest_path_to_sanction is None
                else self.shortest_path_to_sanction.to_dict(),

            "ownership_chain":
                None if self.ownership_chain is None
                else self.ownership_chain.to_dict(),

            "circular_paths":
                [
                    p.to_dict()
                    for p in self.circular_paths
                ],

            "total_paths":
                self.total_paths,

            "graph_risk_score":
                self.graph_risk_score,
        }