"""
==========================================================
AML Investigation Platform

Entity Extractor

Responsibilities
----------------
✓ Extract graph entities
✓ Build EntityMetadata
✓ Use semantic metadata
✓ Use key metadata

==========================================================
"""

from __future__ import annotations

from app.models.graph.entity_metadata import EntityMetadata
from app.models.schema.table_metadata import TableMetadata


class EntityExtractor:
    """
    Extract graph entities from table metadata.
    """

    @classmethod
    def extract(
        cls,
        table: TableMetadata,
    ) -> list[EntityMetadata]:

        entities: list[EntityMetadata] = []

        for column in table.columns:

            if column.semantic is None:
                continue

            semantic = column.semantic.semantic_type

            if semantic == "UNKNOWN":
                continue

            entity = EntityMetadata(

                entity_type=semantic,

                node_label=semantic.replace("_ID", "").title(),

                display_name=column.name,

                identifier_property=column.name,

                identifier_value=column.name,

                source_table=table.table_name,

                source_column=column.name,

                primary_identifier=column.primary_key,

                confidence=column.semantic.confidence,

                properties={

                    "sql_type": column.sql_type,

                    "nullable": column.nullable,

                    "unique": column.unique,

                },

                aliases=[column.original_name],

                evidence=[
                    f"Detected as '{semantic}'"
                ],
            )

            entities.append(entity)

        return entities