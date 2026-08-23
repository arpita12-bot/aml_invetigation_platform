"""
==========================================================
AML Investigation Platform

DDL Generator

Responsibilities
----------------
✓ Generate CREATE TABLE statements
✓ Generate column definitions
✓ Apply primary keys
✓ Apply foreign keys
✓ Apply constraints
✓ Produce PostgreSQL-compatible DDL

==========================================================
"""

from __future__ import annotations

from app.models.schema.dataset_metadata import DatasetMetadata
from app.models.schema.column_metadata import ColumnMetadata
from app.services.database.sql_type_mapper import SQLTypeMapper
from app.models.database.ddl_statement import DDLStatement
from app.core.enums import DDLStatementType
from app.services.database.constraint_generator import (
    ConstraintGenerator,
)
from app.services.database.index_generator import IndexGenerator

class DDLGenerator:
    """
    Generates PostgreSQL DDL statements
    from DatasetMetadata.
    """

    @classmethod
    def generate_create_table(
    cls,
    metadata: DatasetMetadata,
    ) -> list[DDLStatement]:

        table = metadata.table

        lines: list[str] = []

        # --------------------------------------------------
        # Columns
        # --------------------------------------------------

        print("\n========== DDL DEBUG ==========")

        for column in table.columns:

            print(f"Column Type : {type(column)}")
            print(f"Name        : {column.name}")
            print(f"SQL Type    : {column.sql_type}")
            print("--------------------------------")

            column_sql = cls._column_definition(column)

            print("Generated SQL:", column_sql)

            lines.append(column_sql)
        # --------------------------------------------------
        # Primary Keys
        # --------------------------------------------------

        primary_key = ConstraintGenerator.primary_key(
            table
        )

        if primary_key:

            lines.append(primary_key)

        # --------------------------------------------------
        # Foreign Keys
        # --------------------------------------------------

        lines.extend(

            ConstraintGenerator.foreign_keys(
                table
            )

        )

        ddl = (
            f"CREATE TABLE IF NOT EXISTS {table.table_name} (\n"
            + ",\n".join(
                f"    {line}"
                for line in lines
            )
            + "\n);"
        )

        statements = [

            DDLStatement(

                statement_type=DDLStatementType.CREATE_TABLE,

                sql=ddl,

                table_name=table.table_name,

                execution_order=1,

                description=f"Create table {table.table_name}",

            )

        ]

        statements.extend(

            IndexGenerator.generate(table)

        )

        return statements

    @classmethod
    def _column_definition(
        cls,
        column: ColumnMetadata,
    ) -> str:

        sql_type = SQLTypeMapper.postgres_type(column)

        parts = [
            column.name,
            sql_type,
        ]

        # --------------------------------------------------
        # Auto Increment
        # --------------------------------------------------

        if column.auto_increment:

            # If using PostgreSQL SERIAL/BIGSERIAL,
            # SQLTypeMapper should already return the
            # appropriate type.
            pass

        # --------------------------------------------------
        # Column Constraints
        # --------------------------------------------------

        parts.extend(
            ConstraintGenerator.column_constraints(column)
        )

        definition = " ".join(
            str(part)
            for part in parts
            if part not in (None, "")
        )

        print(f"Generated Column: {definition}")

        return definition