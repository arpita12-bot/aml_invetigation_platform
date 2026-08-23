"""
==========================================================
AML Investigation Platform

Dataset Metadata

Master metadata object representing everything
known about an uploaded dataset.

Shared Across

✓ Schema Inference
✓ PostgreSQL Builder
✓ Neo4j Builder
✓ Entity Resolution
✓ Dashboard
✓ Knowledge Graph
✓ Feature Engineering

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.profile.dataset_profile import DatasetProfile
from app.models.schema.graph_metadata import GraphMetadata
from app.models.schema.table_metadata import TableMetadata



@dataclass(slots=True)
class DatasetMetadata:
    """
    Master metadata object.
    """

    table: TableMetadata

    graph: GraphMetadata

    profile: DatasetProfile | None = None

    validation: ValidationSummary | None = None

    def to_dict(self) -> dict:

        return {

            "table": self.table.to_dict(),

            "graph": self.graph.to_dict(),

            "profile": (
                self.profile.to_dict()
                if self.profile
                else None
            ),

            "validation": (
                self.validation.to_dict()
                if self.validation
                else None
            ),

        }