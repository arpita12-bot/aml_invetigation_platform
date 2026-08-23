"""
==========================================================
AML Investigation Platform

Investigation Graph Metadata

Responsibilities
----------------
✓ Graph statistics
✓ Investigation metadata
✓ Execution metadata

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class InvestigationGraphMetadata:
    """
    Metadata describing an investigation graph.
    """

    graph_name: str = ""

    node_count: int = 0

    relationship_count: int = 0

    path_count: int = 0

    shell_candidate_count: int = 0

    generated_at: datetime | None = None