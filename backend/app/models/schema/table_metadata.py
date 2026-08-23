"""
==========================================================
AML Investigation Platform

Table Metadata

Represents metadata inferred for an uploaded dataset.

Shared Across

✓ Schema Inference
✓ PostgreSQL Builder
✓ Dataset Registry
✓ Neo4j Builder
✓ Entity Resolution
✓ Dashboard

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.schema.column_metadata import ColumnMetadata
from app.models.schema.key_metadata import KeyMetadata
from app.models.schema.relationship_metadata import RelationshipMetadata


@dataclass(slots=True)
class TableMetadata:
    """
    Metadata describing an uploaded dataset.
    """

    # =====================================================
    # Dataset Information
    # =====================================================

    dataset_name: str

    original_filename: str

    table_name: str

    dataset_type: str = "UNKNOWN"

    description: str = ""

    source: str = ""

    version: int = 1

    # =====================================================
    # Table Statistics
    # =====================================================

    row_count: int = 0

    column_count: int = 0

    file_size_mb: float = 0.0

    memory_usage_mb: float = 0.0

    duplicate_rows: int = 0

    missing_values: int = 0

    quality_score: float = 100.0

    # =====================================================
    # Schema
    # =====================================================

    columns: list[ColumnMetadata] = field(
        default_factory=list
    )

    # =====================================================
    # Keys
    # =====================================================

    keys: list[KeyMetadata] = field(
        default_factory=list
    )
    # =====================================================
    # Relationships
    # =====================================================

    relationships: list[RelationshipMetadata] = field(
        default_factory=list
    )

    # =====================================================
    # Neo4j
    # =====================================================

    node_labels: list[str] = field(
        default_factory=list
    )

    relationship_labels: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Validation
    # =====================================================

    validation_errors: list[str] = field(
        default_factory=list
    )

    validation_warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    @property
    def nullable_columns(self) -> list[str]:
        """
        Return nullable columns.
        """
        return [
            column.name
            for column in self.columns
            if column.nullable
        ]

    @property
    def required_columns(self) -> list[str]:
        """
        Return NOT NULL columns.
        """
        return [
            column.name
            for column in self.columns
            if not column.nullable
        ]

    @property
    def unique_columns(self) -> list[str]:
        """
        Return UNIQUE columns.
        """
        return [
            column.name
            for column in self.columns
            if column.unique
        ]

    @property
    def column_names(self) -> list[str]:
        """
        Return all column names.
        """
        return [
            column.name
            for column in self.columns
        ]

    def get_column(
        self,
        column_name: str,
    ) -> ColumnMetadata | None:
        """
        Retrieve metadata for one column.
        """
        for column in self.columns:

            if column.name == column_name:

                return column

        return None

    def has_column(
        self,
        column_name: str,
    ) -> bool:

        return any(
            column.name == column_name
            for column in self.columns
        )

    def add_column(
        self,
        column: ColumnMetadata,
    ) -> None:

        self.columns.append(column)

        self.column_count = len(self.columns)

    def remove_column(
        self,
        column_name: str,
    ) -> None:

        self.columns = [

            column

            for column in self.columns

            if column.name != column_name

        ]

        self.column_count = len(self.columns)

    def to_dict(self) -> dict:

        return {

            "dataset_name": self.dataset_name,

            "original_filename": self.original_filename,

            "table_name": self.table_name,

            "dataset_type": self.dataset_type,

            "description": self.description,

            "source": self.source,

            "version": self.version,

            "row_count": self.row_count,

            "column_count": self.column_count,

            "file_size_mb": self.file_size_mb,

            "memory_usage_mb": self.memory_usage_mb,

            "duplicate_rows": self.duplicate_rows,

            "missing_values": self.missing_values,

            "quality_score": self.quality_score,

            "keys": [
                key.to_dict()
                for key in self.keys
            ],

            "relationships": [

                relationship.to_dict()

                for relationship in self.relationships

            ],

            "node_labels": self.node_labels,

            "relationship_labels": self.relationship_labels,

            "validation_errors": self.validation_errors,

            "validation_warnings": self.validation_warnings,

            "columns": [
                column.to_dict()
                for column in self.columns
            ],

        }
        
    @property
    def primary_keys(self) -> list[KeyMetadata]:
        return [
            key
            for key in self.keys
            if str(key.key_type).upper() == "PRIMARY"
        ]


    @property
    def foreign_keys(self) -> list[KeyMetadata]:
        return [
            key
            for key in self.keys
            if str(key.key_type).upper() == "FOREIGN"
        ]


    @property
    def candidate_keys(self) -> list[KeyMetadata]:
        return [
            key
            for key in self.keys
            if str(key.key_type).upper() == "CANDIDATE"
        ]


    def add_key(
        self,
        key: KeyMetadata,
    ) -> None:

        self.keys.append(key)
        
    # =====================================================
    # Relationship Helpers
    # =====================================================

    @property
    def related_tables(self) -> list[str]:
        """
        Return all unique tables related to this dataset.
        """

        return sorted({

            relationship.target_table

            for relationship in self.relationships

            if relationship.target_table

        })


    def add_relationship(
        self,
        relationship: RelationshipMetadata,
    ) -> None:
        """
        Add a relationship.
        """

        self.relationships.append(
            relationship
        )


    def get_relationships(
        self,
        target_table: str | None = None,
    ) -> list[RelationshipMetadata]:
        """
        Return relationships.

        If target_table is provided,
        return only matching relationships.
        """

        if target_table is None:

            return self.relationships

        return [

            relationship

            for relationship in self.relationships

            if relationship.target_table == target_table

        ]