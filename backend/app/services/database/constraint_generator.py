"""
==========================================================
AML Investigation Platform

Constraint Generator
==========================================================
"""

from __future__ import annotations

from app.models.schema.table_metadata import TableMetadata
from app.models.schema.column_metadata import ColumnMetadata


class ConstraintGenerator:

    @classmethod
    def primary_key(
        cls,
        table: TableMetadata,
    ) -> str | None:

        primary_keys = [
            key.column_name
            for key in table.primary_keys
        ]

        if not primary_keys:
            return None

        return f"PRIMARY KEY ({', '.join(primary_keys)})"

    @classmethod
    def foreign_keys(
        cls,
        table: TableMetadata,
    ) -> list[str]:

        constraints: list[str] = []

        for key in table.foreign_keys:

            if (
                key.referenced_table
                and key.referenced_column
            ):

                constraints.append(
                    f"FOREIGN KEY ({key.column_name}) "
                    f"REFERENCES {key.referenced_table}"
                    f"({key.referenced_column})"
                )

        return constraints

    @classmethod
    def column_constraints(
        cls,
        column: ColumnMetadata,
    ) -> list[str]:

        constraints: list[str] = []

        if not column.nullable:
            constraints.append("NOT NULL")

        if column.unique:
            constraints.append("UNIQUE")

        if column.default_value is not None:

            if isinstance(column.default_value, str):
                constraints.append(
                    f"DEFAULT '{column.default_value}'"
                )
            else:
                constraints.append(
                    f"DEFAULT {column.default_value}"
                )

        if column.check_constraint:
            constraints.append(
                f"CHECK ({column.check_constraint})"
            )

        return constraints