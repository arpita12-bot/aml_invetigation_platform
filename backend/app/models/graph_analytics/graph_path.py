"""
==========================================================
AML Investigation Platform

Graph Path

Represents a path between two entities
inside the Knowledge Graph.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphPath:
    """
    Graph traversal result.
    """

    source: str

    target: str

    path: list[str] = field(default_factory=list)

    relationships: list[str] = field(default_factory=list)

    length: int = 0

    risk_score: float = 0.0

    def to_dict(self) -> dict:

        return {

            "source": self.source,

            "target": self.target,

            "path": self.path,

            "relationships": self.relationships,

            "length": self.length,

            "risk_score": self.risk_score,
        }