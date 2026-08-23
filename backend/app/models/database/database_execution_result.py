"""
==========================================================
AML Investigation Platform

Database Execution Result

Represents the outcome of executing
DDL/DML statements.

Shared Across

✓ PostgreSQL Builder
✓ Bulk Loader
✓ Schema Deployment
✓ Dashboard

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DatabaseExecutionResult:
    """
    Result of database execution.
    """

    successful: bool = True

    executed_statements: int = 0

    failed_statement: str | None = None

    execution_time_ms: float = 0.0

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:

        return {

            "successful": self.successful,

            "executed_statements": self.executed_statements,

            "failed_statement": self.failed_statement,

            "execution_time_ms": self.execution_time_ms,

            "errors": self.errors,

            "warnings": self.warnings,

        }