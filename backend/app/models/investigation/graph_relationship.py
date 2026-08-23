"""
==========================================================
AML Investigation Platform

Graph Relationship

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GraphRelationship:
    """
    Generic relationship inside an investigation graph.
    """

    relationship_type: str

    source_id: str

    target_id: str

    properties: dict[str, Any] = field(
        default_factory=dict
    )