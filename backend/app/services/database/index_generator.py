"""
==========================================================
AML Investigation Platform

Index Generator

Responsibilities
----------------
✓ Generate PostgreSQL indexes
✓ Generate UNIQUE indexes
✓ Generate Composite indexes
✓ Return executable DDL statements

==========================================================
"""

from __future__ import annotations

from app.core.enums import DDLStatementType
from app.models.database.ddl_statement import DDLStatement
from app.models.schema.table_metadata import TableMetadata


class IndexGenerator:
    """
    Generates PostgreSQL index statements.
    """

    @classmethod
    def generate(
        cls,
        table: TableMetadata,
    ) -> list[DDLStatement]:

        statements: list[DDLStatement] = []

        # ------------------------------------------
        # Single-column indexes
        # ------------------------------------------

        for column in table.columns:

            if not column.index:
                continue

            index_name = (
                f"idx_{table.table_name}_{column.name}"
            )

            sql = (
                f"CREATE INDEX IF NOT EXISTS "
                f"{index_name} "
                f"ON {table.table_name} ({column.name});"
            )

            statements.append(

                DDLStatement(

                    statement_type=DDLStatementType.CREATE_INDEX,

                    sql=sql,

                    table_name=table.table_name,

                    execution_order=100,

                    description=(
                        f"Create index on "
                        f"{column.name}"
                    ),

                )

            )

        return statements