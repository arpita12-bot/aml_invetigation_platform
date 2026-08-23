"""
==========================================================
AML Investigation Platform

Column Metadata

Represents metadata inferred for a single dataset column.

This model is shared across:

✓ Schema Inference
✓ PostgreSQL Builder
✓ Neo4j Builder
✓ Entity Resolution
✓ Feature Engineering
✓ Dashboard

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from app.models.schema.semantic_metadata import SemanticMetadata

@dataclass(slots=True)
class ColumnMetadata:
    """
    Metadata describing one dataset column.
    """

    # --------------------------------------------
    # Basic Information
    # --------------------------------------------

    name: str

    original_name: str

    semantic: SemanticMetadata | None = None

    # --------------------------------------------
    # PostgreSQL Information
    # --------------------------------------------

    sql_type: str = "TEXT"

    nullable: bool = True

    unique: bool = False

    primary_key: bool = False

    foreign_key: bool = False

    referenced_table: str | None = None

    referenced_column: str | None = None
    
    # --------------------------------------------
    # Database / DDL Metadata
    # --------------------------------------------

    # Default value assigned to the column
    default_value: Any | None = None

    # SQL CHECK constraint expression
    check_constraint: str | None = None

    # Whether an index should be created
    index: bool = False

    # Identity / SERIAL column
    auto_increment: bool = False

    # Database column comment
    comment: str | None = None
    
    # Column position in the original dataset
    ordinal_position: int = 0

    # Whether the column should participate in graph node properties
    graph_property: bool = True

    # --------------------------------------------
    # Data Profiling
    # --------------------------------------------

    max_length: int = 0

    min_length: int = 0

    distinct_count: int = 0

    null_count: int = 0

    duplicate_count: int = 0

    sample_values: list[Any] = field(
        default_factory=list
    )

    # --------------------------------------------
    # Statistics
    # --------------------------------------------

    minimum: Any | None = None

    maximum: Any | None = None

    mean: float | None = None

    median: float | None = None

    std_dev: float | None = None

    # --------------------------------------------
    # Neo4j
    # --------------------------------------------

    node_property: bool = True

    relationship_property: bool = False

    # --------------------------------------------
    # Validation
    # --------------------------------------------

    quality_score: float = 100.0

    validation_errors: list[str] = field(
        default_factory=list
    )

    validation_warnings: list[str] = field(
        default_factory=list
    )

    # --------------------------------------------
    # Helper Methods
    # --------------------------------------------

    @property
    def completeness(self) -> float:
        """
        Percentage of non-null values.
        """
        total = self.distinct_count + self.null_count

        if total == 0:
            return 100.0

        return round(
            ((total - self.null_count) / total) * 100,
            2,
        )

    @property
    def uniqueness(self) -> float:
        """
        Percentage of unique values.
        """
        total = self.distinct_count + self.duplicate_count

        if total == 0:
            return 100.0

        return round(
            (self.distinct_count / total) * 100,
            2,
        )

    def to_dict(self) -> dict:
        """
        Serialize metadata.
        """

        return {

            "name": self.name,

            "original_name": self.original_name,

            "semantic": (
                self.semantic.to_dict()
                if self.semantic
                else None
            ),

            "sql_type": self.sql_type,

            "nullable": self.nullable,

            "unique": self.unique,

            "primary_key": self.primary_key,

            "foreign_key": self.foreign_key,

            "referenced_table": self.referenced_table,

            "referenced_column": self.referenced_column,
            
            "default_value": self.default_value,

            "check_constraint": self.check_constraint,

            "index": self.index,
            
            "ordinal_position": self.ordinal_position,
            
            "graph_property": self.graph_property,

            "auto_increment": self.auto_increment,

            "comment": self.comment,

            "max_length": self.max_length,

            "min_length": self.min_length,

            "distinct_count": self.distinct_count,

            "null_count": self.null_count,

            "duplicate_count": self.duplicate_count,

            "sample_values": self.sample_values,

            "minimum": self.minimum,

            "maximum": self.maximum,

            "mean": self.mean,

            "median": self.median,

            "std_dev": self.std_dev,

            "node_property": self.node_property,

            "relationship_property": self.relationship_property,

            "quality_score": self.quality_score,

            "validation_errors": self.validation_errors,

            "validation_warnings": self.validation_warnings,

        }
        
    @property
    def semantic_type(self) -> str:

        if self.semantic is None:

            return "UNKNOWN"

        return self.semantic.semantic_type