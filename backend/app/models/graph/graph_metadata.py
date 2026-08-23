"""
==========================================================
AML Investigation Platform

Graph Metadata

Enterprise Graph Representation

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.graph.entity_metadata import EntityMetadata
from app.models.schema.relationship_metadata import RelationshipMetadata


@dataclass(slots=True)
class GraphMetadata:

    # ======================================================
    # Graph Identity
    # ======================================================

    graph_name: str

    source_dataset: str

    directed: bool = True

    # ======================================================
    # Graph Content
    # ======================================================

    entities: list[EntityMetadata] = field(
        default_factory=list
    )

    relationships: list[RelationshipMetadata] = field(
        default_factory=list
    )

    # ======================================================
    # Enterprise Indexes
    # ======================================================

    entities_by_label: dict[
        str,
        list[EntityMetadata]
    ] = field(default_factory=dict)

    entities_by_identifier: dict[
        tuple[str, str],
        EntityMetadata,
    ] = field(default_factory=dict)

    # ======================================================
    # Statistics
    # ======================================================

    node_count: int = 0

    edge_count: int = 0

    entity_types: dict[str, int] = field(
        default_factory=dict
    )

    relationship_types: dict[str, int] = field(
        default_factory=dict
    )

    properties: dict = field(
        default_factory=dict
    )