from __future__ import annotations

from app.models.schema.column_metadata import ColumnMetadata


class SQLTypeMapper:
    """
    Maps inferred SQL types to PostgreSQL types.
    """

    TYPE_MAPPING = {
        "INTEGER": "INTEGER",
        "INT": "INTEGER",
        "BIGINT": "BIGINT",
        "SMALLINT": "SMALLINT",
        "FLOAT": "DOUBLE PRECISION",
        "DOUBLE": "DOUBLE PRECISION",
        "DOUBLE PRECISION": "DOUBLE PRECISION",
        "DECIMAL": "NUMERIC",
        "NUMERIC": "NUMERIC",
        "BOOLEAN": "BOOLEAN",
        "BOOL": "BOOLEAN",
        "TIMESTAMP": "TIMESTAMP",
        "DATE": "DATE",
        "TEXT": "TEXT",
        "STRING": "TEXT",
        "OBJECT": "TEXT",
    }

    @classmethod
    def postgres_type(
        cls,
        column: ColumnMetadata,
    ) -> str:

        sql_type = (column.sql_type or "TEXT").strip().upper()

        if sql_type.startswith("VARCHAR"):
            return sql_type

        return cls.TYPE_MAPPING.get(sql_type, "TEXT")