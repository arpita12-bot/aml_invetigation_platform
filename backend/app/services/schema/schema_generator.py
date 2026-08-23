"""
==========================================================
AML Investigation Platform

Schema Generator

Responsibilities
----------------
✓ Build TableMetadata
✓ Assemble Column Metadata
✓ Assemble Key Metadata
✓ Prepare Relationship Metadata

==========================================================
"""

from __future__ import annotations

from app.models.schema.column_metadata import ColumnMetadata
from app.models.schema.relationship_metadata import RelationshipMetadata
from app.models.schema.table_metadata import TableMetadata
from app.models.schema.key_metadata import KeyMetadata

class SchemaGenerator:
    """
    Creates a complete TableMetadata object
    from inferred metadata.
    """

    @classmethod
    def generate(
        cls,
        *,
        dataset_name: str,
        original_filename: str,
        table_name: str,
        dataset_type: str,
        row_count: int,
        file_size_mb: float,
        columns: list[ColumnMetadata],
        keys: list[KeyMetadata],
        relationships: list[RelationshipMetadata] | None = None,
        description: str = "",
        source: str = "",
    ) -> TableMetadata:

        if relationships is None:
            relationships = []

        table = TableMetadata(

            dataset_name=dataset_name,

            original_filename=original_filename,

            table_name=table_name,

            dataset_type=dataset_type,

            description=description,

            source=source,

            row_count=row_count,

            column_count=len(columns),

            file_size_mb=file_size_mb,

            columns=columns,

            keys=keys,

            relationships=relationships,

        )

        return table