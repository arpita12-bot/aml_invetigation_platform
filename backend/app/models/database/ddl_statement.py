"""
==========================================================
AML Investigation Platform

DDL Statement

Represents one SQL statement generated
by the PostgreSQL Builder.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.enums import DDLStatementType


@dataclass(slots=True)
class DDLStatement:
    """
    Represents one executable DDL statement.
    """

    # =====================================================
    # Statement Information
    # =====================================================

    statement_type: DDLStatementType

    sql: str

    table_name: str

    # =====================================================
    # Execution
    # =====================================================

    execution_order: int = 0

    transactional: bool = True

    enabled: bool = True

    # =====================================================
    # Metadata
    # =====================================================

    description: str = ""

    def to_dict(self) -> dict:

        return {

            "statement_type": (
                self.statement_type.value
                if isinstance(
                    self.statement_type,
                    DDLStatementType,
                )
                else str(self.statement_type)
            ),

            "sql": self.sql,

            "table_name": self.table_name,

            "execution_order": self.execution_order,

            "transactional": self.transactional,

            "enabled": self.enabled,

            "description": self.description,

        }