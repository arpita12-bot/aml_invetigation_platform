"""
==========================================================
AML Investigation Platform

Bulk Loader

Responsibilities
----------------
✓ Batch insert
✓ Transaction management
✓ Progress reporting

==========================================================
"""

from __future__ import annotations

import time

import pandas as pd
from sqlalchemy.orm import Session

from app.models.database.database_execution_result import (
    DatabaseExecutionResult,
)

from app.services.database.batch_generator import (
    BatchGenerator,
)

from app.services.database.bulk_insert_executor import (
    BulkInsertExecutor,
)


class BulkLoader:

    @classmethod
    def load(
        cls,
        *,
        session: Session,
        dataframe: pd.DataFrame,
        table_name: str,
        batch_size: int = 5000,
    ) -> DatabaseExecutionResult:

        start = time.perf_counter()

        result = DatabaseExecutionResult()

        try:

            for batch in BatchGenerator.generate(
                dataframe,
                batch_size,
            ):

                rows = batch.to_dict(
                    orient="records"
                )

                inserted = BulkInsertExecutor.execute(

                    session=session,

                    table_name=table_name,

                    rows=rows,

                )

                result.executed_statements += inserted

            session.commit()

            result.successful = True

        except Exception as ex:

            session.rollback()

            result.successful = False

            result.errors.append(
                str(ex)
            )

        finally:

            result.execution_time_ms = round(

                (time.perf_counter() - start)
                * 1000,

                2,

            )

        return result