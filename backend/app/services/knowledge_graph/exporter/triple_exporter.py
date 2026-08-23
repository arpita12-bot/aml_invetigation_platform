"""
==========================================================
AML Investigation Platform

Triple Exporter

Responsibilities
----------------
✓ Convert graph relationships into triples
✓ Validate triples
✓ Generate statistics
✓ Export TSV / CSV
✓ Return export result

==========================================================
"""

from __future__ import annotations

import csv
import time
from pathlib import Path
from datetime import datetime

from app.models.graph.graph_metadata import GraphMetadata

from app.models.knowledge_graph.triple import Triple
from app.models.knowledge_graph.triple_statistics import (
    TripleStatistics,
)
from app.models.knowledge_graph.triple_export_result import (
    TripleExportResult,
)

from app.services.knowledge_graph.triple_validator import (
    TripleValidator,
)


class TripleExporter:

    @classmethod
    def export(
        cls,
        *,
        graph: GraphMetadata,
        output_directory: str,
        filename: str = "train.tsv",
    ) -> tuple[
        TripleExportResult,
        TripleStatistics,
    ]:

        start = time.perf_counter()

        result = TripleExportResult(

            output_file=str(
                Path(output_directory) / filename
            ),

            started_at=datetime.utcnow(),
        )

        # --------------------------------------------------
        # Convert Relationships → Triples
        # --------------------------------------------------

        triples: list[Triple] = []

        for relationship in graph.relationships:

            triples.append(

                Triple(

                    head=
                        relationship.source_identifier_value,

                    relation=
                        relationship.relationship_type,

                    tail=
                        relationship.target_identifier_value,

                    confidence=
                        relationship.confidence,

                    source_table=
                        relationship.source_table,

                    target_table=
                        relationship.target_table,

                    inferred=
                        relationship.inferred,

                    properties=
                        relationship.properties,

                )

            )

        result.total_triples = len(triples)

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        (
            triples,
            warnings,
            duplicate_count,
        ) = TripleValidator.validate(triples)

        result.warnings.extend(warnings)

        result.duplicate_triples = duplicate_count

        result.exported_triples = len(triples)

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        relation_frequency = {}

        entity_frequency = {}

        entities = set()

        for triple in triples:

            entities.add(triple.head)

            entities.add(triple.tail)

            relation_frequency[
                triple.relation
            ] = relation_frequency.get(
                triple.relation,
                0,
            ) + 1

            entity_frequency[
                triple.head
            ] = entity_frequency.get(
                triple.head,
                0,
            ) + 1

            entity_frequency[
                triple.tail
            ] = entity_frequency.get(
                triple.tail,
                0,
            ) + 1

        statistics = TripleStatistics(

            total_entities=len(entities),

            total_relations=len(
                relation_frequency
            ),

            total_triples=len(triples),

            unique_heads=len(

                {

                    t.head

                    for t in triples

                }

            ),

            unique_tails=len(

                {

                    t.tail

                    for t in triples

                }

            ),

            relation_frequency=relation_frequency,

            entity_frequency=entity_frequency,

        )

        # --------------------------------------------------
        # Export TSV
        # --------------------------------------------------

        output_path = Path(output_directory)

        output_path.mkdir(

            parents=True,

            exist_ok=True,

        )

        file_path = output_path / filename

        with open(

            file_path,

            "w",

            newline="",

            encoding="utf-8",

        ) as file:

            writer = csv.writer(

                file,

                delimiter="\t",

            )

            for triple in triples:

                writer.writerow(

                    [

                        triple.head,

                        triple.relation,

                        triple.tail,

                    ]

                )

        result.finished_at = datetime.utcnow()

        result.execution_time_seconds = (

            time.perf_counter() - start

        )

        return result, statistics