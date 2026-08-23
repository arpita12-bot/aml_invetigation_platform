"""
==========================================================
AML Investigation Platform

Relationship Deduplicator

Responsibilities
----------------
✓ Remove duplicate relationships
✓ Preserve discovery order
✓ Keep first occurrence
✓ Domain independent

==========================================================
"""

from __future__ import annotations

from app.models.schema.relationship_metadata import (
    RelationshipMetadata,
)


class RelationshipDeduplicator:
    """
    Removes duplicate relationships discovered from
    multiple providers.
    """

    def deduplicate(
        self,
        relationships: list[RelationshipMetadata],
    ) -> list[RelationshipMetadata]:

        seen: set[tuple] = set()

        unique: list[RelationshipMetadata] = []

        for relationship in relationships:

            key = self._build_key(relationship)

            if key in seen:
                continue

            seen.add(key)

            unique.append(relationship)

        return unique

    @staticmethod
    def _build_key(
        relationship: RelationshipMetadata,
    ) -> tuple:

        return (

            relationship.source_table,

            relationship.source_column,

            relationship.target_table,

            relationship.target_column,

            relationship.relationship_type,

        )