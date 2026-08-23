"""
==========================================================
AML Investigation Platform

Knowledge Graph Dataset

Represents a dataset ready for embedding models.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from app.models.knowledge_graph.triple import Triple


@dataclass(slots=True)
class KnowledgeGraphDataset:
    """
    In-memory representation of a knowledge graph dataset.
    """

    dataset_name: str

    triples: list[Triple] = field(
        default_factory=list
    )

    entity_to_id: dict[str, int] = field(
        default_factory=dict
    )

    relation_to_id: dict[str, int] = field(
        default_factory=dict
    )

    source_file: str = ""

    @property
    def total_triples(self) -> int:
        return len(self.triples)

    @property
    def total_entities(self) -> int:
        return len(self.entity_to_id)

    @property
    def total_relations(self) -> int:
        return len(self.relation_to_id)

    @property
    def dataset_path(self) -> Path:
        return Path(self.source_file)