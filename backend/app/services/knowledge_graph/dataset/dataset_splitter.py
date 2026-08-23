"""
==========================================================
AML Investigation Platform

Knowledge Graph Dataset Splitter

Responsibilities
----------------
✓ Random train/validation/test split
✓ Reproducible datasets
✓ Enterprise dataset preparation

==========================================================
"""

from __future__ import annotations

import random

from app.models.knowledge_graph.triple import Triple

from app.models.knowledge_graph.dataset_split import (
    DatasetSplit,
)

from app.models.knowledge_graph.knowledge_graph_dataset import (
    KnowledgeGraphDataset,
)


class DatasetSplitter:

    @classmethod
    def split(
        cls,
        *,
        dataset: KnowledgeGraphDataset,
        train_ratio: float = 0.8,
        validation_ratio: float = 0.1,
        test_ratio: float = 0.1,
        random_seed: int = 42,
    ) -> DatasetSplit:

        if abs(
            train_ratio
            + validation_ratio
            + test_ratio
            - 1.0
        ) > 1e-6:

            raise ValueError(
                "Split ratios must equal 1.0"
            )

        triples = dataset.triples.copy()

        rng = random.Random(random_seed)

        rng.shuffle(triples)

        total = len(triples)

        train_end = int(
            total * train_ratio
        )

        validation_end = train_end + int(
            total * validation_ratio
        )

        train_triples = triples[:train_end]

        validation_triples = triples[
            train_end:validation_end
        ]

        test_triples = triples[
            validation_end:
        ]

        def build_dataset(
            name: str,
            data: list[Triple],
        ) -> KnowledgeGraphDataset:

            return KnowledgeGraphDataset(

                dataset_name=name,

                triples=data,

                entity_to_id=dataset.entity_to_id,

                relation_to_id=dataset.relation_to_id,

                source_file=dataset.source_file,

            )

        return DatasetSplit(

            training=build_dataset(
                "training",
                train_triples,
            ),

            validation=build_dataset(
                "validation",
                validation_triples,
            ),

            testing=build_dataset(
                "testing",
                test_triples,
            ),

            random_seed=random_seed,

            train_ratio=train_ratio,

            validation_ratio=validation_ratio,

            test_ratio=test_ratio,

        )