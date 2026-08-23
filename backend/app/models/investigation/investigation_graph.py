"""
==========================================================
AML Investigation Platform

Investigation Graph

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.graph_analytics.graph_path import (
    GraphPath,
)

from app.models.investigation.graph_node import (
    GraphNode,
)

from app.models.investigation.graph_relationship import (
    GraphRelationship,
)

from app.models.investigation.investigation_graph_metadata import (
    InvestigationGraphMetadata,
)

from app.models.shell_pattern_candidate import (
    ShellPatternCandidate,
)


@dataclass(slots=True)
class InvestigationGraph:
    """
    Complete graph collected for one AML investigation.
    """

    root_entity_id: str

    nodes: list[GraphNode] = field(
        default_factory=list
    )

    relationships: list[GraphRelationship] = field(
        default_factory=list
    )

    paths: list[GraphPath] = field(
        default_factory=list
    )

    shell_candidates: list[
        ShellPatternCandidate
    ] = field(
        default_factory=list
    )

    metadata: InvestigationGraphMetadata = field(
        default_factory=InvestigationGraphMetadata
    )