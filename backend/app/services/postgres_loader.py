"""
==========================================================
AML Investigation Platform

Enterprise PostgreSQL Loader

Responsibilities
----------------
✓ Bulk insert
✓ Chunk loading
✓ Append / Replace loading
✓ Transaction management
✓ Retry mechanism
✓ Statistics
✓ Rollback support
✓ Performance monitoring

==========================================================
"""

from __future__ import annotations

import logging
import math
import time
from sqlalchemy import text
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.services.dynamic_table_creator import DynamicTableCreator

logger = logging.getLogger(__name__)

class PostgresLoader:
    """
    Enterprise PostgreSQL Bulk Loader
    """

    DEFAULT_BATCH_SIZE = 5000

    MAX_RETRIES = 3

    def __init__(
        self,
        db: Session,
        table_creator: Optional[DynamicTableCreator] = None,
    ):

        self.db = db

        self.engine = db.get_bind()

        self.metadata = MetaData()

        self.table_creator = (
            table_creator
            if table_creator
            else DynamicTableCreator(db)
        )
        
        # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_dataframe(
        self,
        df: pd.DataFrame,
    ):

        if df.empty:
            raise ValueError(
                "Cannot load an empty dataframe."
            )

        if len(df.columns) == 0:
            raise ValueError(
                "Dataframe has no columns."
            )

    def validate_table(
        self,
        table_name: str,
    ):

        if not self.table_creator.table_exists(table_name):

            raise ValueError(

                f"Table '{table_name}' does not exist."

            )
            
    # ---------------------------------------------------------
    # Insert One Chunk
    # ---------------------------------------------------------

    def insert_chunk(
            self,
            table: Table,
            chunk: pd.DataFrame,
        ) -> int:
            """
            Insert one dataframe chunk into PostgreSQL.

            Automatically ignores dataframe columns that do not
            exist in the target PostgreSQL table.
            """

            if chunk.empty:
                return 0

            # Get actual table columns
            table_columns = {
                column.name
                for column in table.columns
            }

            # Keep only columns that exist in the table
            chunk = chunk[
                [
                    column
                    for column in chunk.columns
                    if column in table_columns
                ]
            ]

            # Nothing to insert
            if chunk.empty:
                logger.warning(
                    "No matching columns found for table '%s'.",
                    table.name,
                )
                return 0

            records = chunk.to_dict(
                orient="records"
            )

            self.db.execute(
                table.insert(),
                records,
            )

            return len(records)
                
    # ---------------------------------------------------------
    # Chunk Generator
    # ---------------------------------------------------------

    def chunk_dataframe(
        self,
        df: pd.DataFrame,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> Generator[pd.DataFrame, None, None]:

        total = len(df)

        for start in range(
            0,
            total,
            batch_size,
        ):

            end = start + batch_size

            yield df.iloc[start:end]
            
    # ---------------------------------------------------------
    # Prepare Data
    # ---------------------------------------------------------

    def prepare_dataframe(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df.replace(
            {
                np.nan: None,
            },
            inplace=True,
        )

        return df
    
    # ---------------------------------------------------------
    # Load Table
    # ---------------------------------------------------------

    def load_table(
        self,
        table_name: str,
    ) -> Table:

        self.validate_table(table_name)

        return self.table_creator.load_table(
            table_name
        )
        
    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        rows: int,
        duration: float,
        table: str,
    ) -> Dict:

        return {

            "table": table,

            "rows_loaded": rows,

            "duration_seconds": round(
                duration,
                2,
            ),

            "rows_per_second": round(
                rows / duration,
                2,
            )
            if duration
            else rows,

        }
        
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health_check(self):

        return {

            "engine": str(self.engine.url),

            "batch_size": self.DEFAULT_BATCH_SIZE,

            "retries": self.MAX_RETRIES,

        }
        
    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health_check(self):

        return {

            "engine": str(self.engine.url),

            "batch_size": self.DEFAULT_BATCH_SIZE,

            "retries": self.MAX_RETRIES,

        }
        
    # ---------------------------------------------------------
    # Bulk Insert
    # ---------------------------------------------------------

    def bulk_insert(
        self,
        table_name: str,
        df: pd.DataFrame,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> Dict:
        """
        Bulk insert dataframe using batches.
        """

        start = time.time()

        table = self.load_table(table_name)

        df = self.prepare_dataframe(df)

        rows_loaded = 0

        for chunk in self.chunk_dataframe(
            df,
            batch_size,
        ):

            rows_loaded += self.insert_chunk(
                table,
                chunk,
            )

        self.db.commit()

        duration = time.time() - start

        logger.info(
            "%s rows loaded into %s",
            rows_loaded,
            table_name,
        )

        return self.statistics(
            rows_loaded,
            duration,
            table_name,
        )
        
    # ---------------------------------------------------------
    # Append
    # ---------------------------------------------------------

    def append_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Dict:
        """
        Append dataframe to existing table.
        """

        self.validate_dataframe(df)

        return self.bulk_insert(
            table_name,
            df,
        )
        
    # ---------------------------------------------------------
    # Truncate
    # ---------------------------------------------------------

    def truncate_table(
        self,
        table_name: str,
    ):
        """
        Remove all rows from table.
        """

        table = self.load_table(table_name)

        self.db.execute(
            delete(table)
        )

        self.db.commit()

        logger.info(
            "Table '%s' truncated.",
            table_name,
        )
    # ---------------------------------------------------------
    # Replace
    # ---------------------------------------------------------

    def replace_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Dict:
        """
        Replace all table data.
        """

        self.truncate_table(
            table_name,
        )

        return self.bulk_insert(
            table_name,
            df,
        )
        
    # ---------------------------------------------------------
    # Main Loader
    # ---------------------------------------------------------

    def load_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        mode: str = "append",
    ) -> Dict:
        """
        Load dataframe into PostgreSQL.

        Modes
        -----
        append
        replace
        """

        mode = mode.lower()

        if mode == "append":

            return self.append_dataframe(
                table_name,
                df,
            )

        if mode == "replace":

            return self.replace_dataframe(
                table_name,
                df,
            )

        raise ValueError(
            f"Unsupported load mode '{mode}'."
        )
        
    # ---------------------------------------------------------
    # Row Count
    # ---------------------------------------------------------

    def row_count(
        self,
        table_name: str,
    ) -> int:
        """
        Return number of rows.
        """

        sql = f'SELECT COUNT(*) FROM "{table_name}"'

        result = self.db.execute(
            text(sql)
        )

        return result.scalar()
    
    # ---------------------------------------------------------
    # Empty Check
    # ---------------------------------------------------------

    def is_empty(
        self,
        table_name: str,
    ) -> bool:

        return self.row_count(
            table_name
        ) == 0
        
        
    # ---------------------------------------------------------
    # Transaction
    # ---------------------------------------------------------

    def rollback(self):
        """
        Roll back current transaction.
        """

        logger.warning(
            "Rolling back transaction."
        )

        self.db.rollback()
        
    def commit(self):
        """
        Commit current transaction.
        """

        self.db.commit()
    
    # ---------------------------------------------------------
    # Retry
    # ---------------------------------------------------------

    def retry_load(
        self,
        table_name: str,
        df: pd.DataFrame,
        mode: str = "append",
        retries: int = 3,
    ):

        for attempt in range(retries):

            try:

                logger.info(
                    "Load attempt %s",
                    attempt + 1,
                )

                return self.load_dataframe(
                    table_name,
                    df,
                    mode,
                )

            except Exception as ex:

                self.rollback()

                logger.exception(ex)

        raise RuntimeError(
            "Loading failed after retries."
    )
        
    # ---------------------------------------------------------
    # Safe Loader
    # ---------------------------------------------------------

    def safe_load(
        self,
        table_name: str,
        df: pd.DataFrame,
        mode: str = "append",
    ):
        """
        Load dataframe with automatic rollback.
        """

        try:

            return self.load_dataframe(
                table_name,
                df,
                mode,
            )

        except Exception:

            self.rollback()

            raise
        
        
    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def load_summary(
        self,
        table_name: str,
    ):
        """
        Return table loading summary.
        """

        return {

            "table": table_name,

            "rows": self.row_count(
                table_name,
            ),

            "empty": self.is_empty(
                table_name,
            ),

        }
        
    # ---------------------------------------------------------
    # Verification
    # ---------------------------------------------------------

    def verify_load(
        self,
        table_name: str,
        expected_rows: int,
    ):

        actual = self.row_count(
            table_name
        )

        return {

            "expected": expected_rows,

            "actual": actual,

            "success": actual == expected_rows,

        }
    
    # ---------------------------------------------------------
    # Delete Data
    # ---------------------------------------------------------

    def delete_all(
        self,
        table_name: str,
    ):

        self.truncate_table(
            table_name,
        )

        logger.info(
            "All rows deleted from %s",
            table_name,
        )
        
    # ---------------------------------------------------------
    # Loader Info
    # ---------------------------------------------------------

    def info(self):

        return {

            "engine": str(self.engine.url),

            "batch_size": self.DEFAULT_BATCH_SIZE,

            "max_retries": self.MAX_RETRIES,

        }