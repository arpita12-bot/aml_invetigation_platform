"""
==========================================================
AML Investigation Platform

Graph Entity Mapper

Responsibilities
----------------
✓ Convert PostgreSQL rows into EntityMetadata
✓ Use business identifier as node identity
✓ Preserve display name
✓ Preserve all business properties

==========================================================
"""

from __future__ import annotations

from app.models.graph.entity_metadata import EntityMetadata


class GraphEntityMapper:

    DISPLAY_FIELDS = [
        "name",
        "full_name",
        "customer_name",
        "company_name",
        "account_name",
    ]

    @classmethod
    def map_row(
        cls,
        *,
        node_label: str,
        identifier_property: str,
        row: dict,
        source_table: str,
    ) -> EntityMetadata:

        # -----------------------------------------
        # Business identifier (Primary Key)
        # -----------------------------------------

        identifier = row.get(identifier_property)

        if identifier is None:
            raise ValueError(
                f"Missing identifier '{identifier_property}' "
                f"for table '{source_table}'."
            )

        identifier = str(identifier)
        # -----------------------------------------
        # Human-readable name
        # -----------------------------------------

        display_name = cls._display_name(row)

        properties = dict(row)

        properties["display_name"] = display_name

        return EntityMetadata(

            entity_type=node_label,

            label=identifier,

            source_table=source_table,

            source_column=identifier_property,

            node_label=node_label,

            primary_identifier=identifier_property,

            confidence=100.0,

            properties=properties,

            aliases=[],

            evidence=[
                "Imported from PostgreSQL"
            ],
        )

    @classmethod
    def _display_name(
        cls,
        row: dict,
    ) -> str:

        for field in cls.DISPLAY_FIELDS:

            value = row.get(field)

            if value not in (None, ""):
                return str(value)

        return "Unknown"