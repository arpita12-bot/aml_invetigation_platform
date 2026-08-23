"""
==========================================================
AML Investigation Platform

PostgreSQL Builder

Responsibilities
----------------
✓ Generate DDL
✓ Execute DDL
✓ Transaction Management
✓ Rollback
✓ Return execution summary

==========================================================
"""

from __future__ import annotations

import logging
import time

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.database.database_execution_result import (
    DatabaseExecutionResult,
)
from app.models.schema.dataset_metadata import DatasetMetadata
from app.services.database.ddl_generator import DDLGenerator


logger = logging.getLogger(__name__)


class PostgresBuilder:
    """
    Creates PostgreSQL tables from metadata.
    """

    @classmethod
    def build(
        cls,
        *,
        session: Session,
        metadata: DatasetMetadata,
    ) -> DatabaseExecutionResult:

        start = time.perf_counter()

        result = DatabaseExecutionResult()

        ddl_statements = DDLGenerator.generate_create_table(
            metadata
        )

        try:

            ddl_statements = sorted(
                ddl_statements,
                key=lambda ddl: ddl.execution_order,
            )

            for statement in ddl_statements:

                if not statement.enabled:
                    continue

                sql = statement.sql.strip()

                if not sql:
                    logger.warning(
                        "Skipping empty DDL statement."
                    )
                    continue

                logger.info(
                    "Executing DDL:\n%s",
                    sql,
                )

                session.execute(text(sql))

                result.executed_statements += 1

            session.commit()

            result.successful = True

        except Exception as ex:

            session.rollback()

            result.successful = False

            result.failed_statement = (
                statement.sql
                if "statement" in locals()
                else None
            )

            logger.exception(
                "DDL execution failed."
            )

            result.errors.append(str(ex))

        finally:

            result.execution_time_ms = round(
                (time.perf_counter() - start) * 1000,
                2,
            )

        return result