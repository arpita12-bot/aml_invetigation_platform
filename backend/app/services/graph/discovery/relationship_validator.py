"""
==========================================================
AML Investigation Platform

Relationship Validator

Responsibilities
----------------
✓ Validate discovered relationships
✓ Verify tables and columns
✓ Verify graph metadata
✓ Populate validation results
✓ Never stop graph generation

==========================================================
"""

from __future__ import annotations

from typing import Iterable

from app.models.schema.relationship_metadata import RelationshipMetadata
from app.models.schema.table_metadata import TableMetadata
from app.services.graph.discovery.metadata_cache import MetadataCache


class RelationshipValidator:
    """
    Validates RelationshipMetadata produced by discovery
    providers.
    """

    def validate(
        self,
        relationships: Iterable[RelationshipMetadata],
        cache: MetadataCache,
        tables: dict[str, TableMetadata],
    ) -> list[RelationshipMetadata]:

        validated: list[RelationshipMetadata] = []

        for relationship in relationships:

            relationship.validation_errors.clear()
            relationship.validation_warnings.clear()
            relationship.valid = True

            self._validate_table(
                relationship.source_table,
                tables,
                "Source",
                relationship,
            )

            self._validate_table(
                relationship.target_table,
                tables,
                "Target",
                relationship,
            )

            self._validate_column(
                relationship.source_table,
                relationship.source_column,
                tables,
                "Source",
                relationship,
            )

            self._validate_column(
                relationship.target_table,
                relationship.target_column,
                tables,
                "Target",
                relationship,
            )

            self._validate_graph_registry(
                relationship.source_table,
                cache,
                "Source",
                relationship,
            )

            self._validate_graph_registry(
                relationship.target_table,
                cache,
                "Target",
                relationship,
            )

            relationship.valid = (
                len(relationship.validation_errors) == 0
            )

            validated.append(relationship)

        return validated

    def _validate_table(
        self,
        table_name: str,
        tables: dict[str, TableMetadata],
        role: str,
        relationship: RelationshipMetadata,
    ) -> None:

        if table_name not in tables:

            relationship.validation_errors.append(
                f"{role} table '{table_name}' not found."
            )

    def _validate_column(
        self,
        table_name: str,
        column_name: str,
        tables: dict[str, TableMetadata],
        role: str,
        relationship: RelationshipMetadata,
    ) -> None:

        table = tables.get(table_name)

        if table is None:
            return

        if not table.has_column(column_name):

            relationship.validation_errors.append(
                f"{role} column '{column_name}' not found in '{table_name}'."
            )

    def _validate_graph_registry(
        self,
        table_name: str,
        cache: MetadataCache,
        role: str,
        relationship: RelationshipMetadata,
    ) -> None:

        if cache.graph(table_name) is None:

            relationship.validation_warnings.append(
                f"{role} table '{table_name}' is not registered for graph generation."
            )