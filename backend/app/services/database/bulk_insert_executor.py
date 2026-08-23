"""
==========================================================
AML Investigation Platform

Bulk Insert Executor

Responsibilities
----------------
✓ Execute one insert batch
✓ Ignore duplicate primary keys
✓ Insert only new records
✓ Return inserted row count

==========================================================
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session


class BulkInsertExecutor:

    @classmethod
    def execute(
        cls,
        *,
        session: Session,
        table_name: str,
        rows: list[dict],
    ) -> int:

        if not rows:
            return 0

        columns = list(rows[0].keys())

        # --------------------------------------------
        # Detect Primary Key
        # --------------------------------------------

        primary_key = columns[0]

        placeholders = ", ".join(
            f":{column}"
            for column in columns
        )

        sql = text(
            f"""
            INSERT INTO {table_name}
            ({", ".join(columns)})
            VALUES
            ({placeholders})
            ON CONFLICT ({primary_key})
            DO NOTHING
            """
        )

        result = session.execute(
            sql,
            rows,
        )

        # Number of newly inserted rows
        return result.rowcount if result.rowcount is not None else 0