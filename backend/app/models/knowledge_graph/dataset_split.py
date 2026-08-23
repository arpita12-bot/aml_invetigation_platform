"""
==========================================================
AML Investigation Platform

Knowledge Graph Dataset Split

Represents Train / Validation / Test datasets.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.knowledge_graph.knowledge_graph_dataset import (
    KnowledgeGraphDataset,
)


@dataclass(slots=True)
class DatasetSplit:
    """
    Represents the split datasets used for
    Knowledge Graph Embedding training.
    """

    training: KnowledgeGraphDataset

    validation: KnowledgeGraphDataset

    testing: KnowledgeGraphDataset

    random_seed: int

    train_ratio: float

    validation_ratio: float

    test_ratio: float

    @property
    def total_triples(self) -> int:

        return (
            self.training.total_triples
            + self.validation.total_triples
            + self.testing.total_triples
        )