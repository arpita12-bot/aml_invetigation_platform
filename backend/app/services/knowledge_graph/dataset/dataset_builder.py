"""
==========================================================
AML Investigation Platform

Knowledge Graph Dataset Builder

Responsibilities
----------------
✓ Read exported triples
✓ Build entity dictionary
✓ Build relation dictionary
✓ Create KnowledgeGraphDataset

==========================================================
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.models.knowledge_graph.triple import Triple
from app.models.knowledge_graph.knowledge_graph_dataset import (
    KnowledgeGraphDataset,
)


class DatasetBuilder:

    @classmethod
    def build(
        cls,
        *,
        dataset_name: str,
        triple_file: str,
    ) -> KnowledgeGraphDataset:
        """
        Build an in-memory knowledge graph dataset from
        an exported TSV file.
        """

        triples: list[Triple] = []

        entities: set[str] = set()

        relations: set[str] = set()

        with open(
            triple_file,
            "r",
            encoding="utf-8",
        ) as file:

            reader = csv.reader(
                file,
                delimiter="\t",
            )

            for row in reader:

                if len(row) != 3:
                    continue

                head, relation, tail = row

                triples.append(
                    Triple(
                        head=head,
                        relation=relation,
                        tail=tail,
                    )
                )

                entities.add(head)
                entities.add(tail)

                relations.add(relation)

        entity_to_id = {
            entity: idx
            for idx, entity in enumerate(
                sorted(entities)
            )
        }

        relation_to_id = {
            relation: idx
            for idx, relation in enumerate(
                sorted(relations)
            )
        }

        return KnowledgeGraphDataset(
            dataset_name=dataset_name,
            triples=triples,
            entity_to_id=entity_to_id,
            relation_to_id=relation_to_id,
            source_file=str(
                Path(triple_file)
            ),
        )