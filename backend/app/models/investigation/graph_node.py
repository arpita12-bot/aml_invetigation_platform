"""
==========================================================
AML Investigation Platform

Graph Node

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GraphNode:
    """
    Generic node inside an investigation graph.
    """

    node_id: str

    label: str

    properties: dict[str, Any] = field(
        default_factory=dict
    )