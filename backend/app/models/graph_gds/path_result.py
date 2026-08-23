"""
==========================================================
AML Investigation Platform

Graph Path Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class GraphPath:

    source_id: str

    target_id: str

    relationship_type: str

    distance: int

    path: list[str]

    risk_score: float