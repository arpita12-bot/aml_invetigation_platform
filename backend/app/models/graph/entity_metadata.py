"""
==========================================================
AML Investigation Platform

Entity Metadata

Represents one entity extracted
from heterogeneous datasets.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EntityMetadata:
    """
    Represents one graph entity.
    """

    # =====================================================
    # Entity
    # =====================================================

    entity_type: str

    label: str

    source_table: str

    source_column: str

    # =====================================================
    # Graph
    # =====================================================

    node_label: str

    primary_identifier: bool = False

    confidence: float = 100.0

    # =====================================================
    # Metadata
    # =====================================================

    properties: dict = field(
        default_factory=dict
    )

    aliases: list[str] = field(
        default_factory=list
    )

    evidence: list[str] = field(
        default_factory=list
    )

    def to_dict(self):

        return {

            "entity_type": self.entity_type,

            "label": self.label,

            "source_table": self.source_table,

            "source_column": self.source_column,

            "node_label": self.node_label,

            "primary_identifier": self.primary_identifier,

            "confidence": self.confidence,

            "properties": self.properties,

            "aliases": self.aliases,

            "evidence": self.evidence,

        }