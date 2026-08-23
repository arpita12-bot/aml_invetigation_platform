"""
==========================================================
AML Investigation Platform

Graph Metric

Represents a single graph algorithm result.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphMetric:

    entity_id: str

    entity_type: str

    algorithm: str

    score: float

    rank: int | None = None

    percentile: float | None = None

    metadata: dict = field(default_factory=dict)