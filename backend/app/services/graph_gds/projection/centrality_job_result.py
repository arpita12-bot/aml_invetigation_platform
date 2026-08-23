"""
==========================================================
AML Investigation Platform

Centrality Job Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.graph_gds.graph_metric import (
    GraphMetric,
)


@dataclass(slots=True)
class CentralityJobResult:

    graph_name: str

    pagerank: list[GraphMetric] = field(
        default_factory=list
    )

    degree: list[GraphMetric] = field(
        default_factory=list
    )

    betweenness: list[GraphMetric] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    successful: bool = False

    execution_time_seconds: float = 0.0