"""
==========================================================
AML Investigation Platform

Dynamic PostgreSQL Table Creator

Enterprise Responsibilities
---------------------------

✓ Dynamic table creation
✓ Dynamic schema generation
✓ SQLAlchemy integration
✓ PostgreSQL type inference
✓ Schema evolution
✓ Reserved keyword handling
✓ Identifier sanitization
✓ Index generation
✓ Transaction management
✓ Metadata driven design

==========================================================
"""

from __future__ import annotations
from sqlalchemy import text
import keyword
import logging
import re
from datetime import date
from datetime import datetime
from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import Index
from sqlalchemy import UniqueConstraint
import time

logger = logging.getLogger(__name__)


class DynamicTableCreator:
    """
    Enterprise Dynamic Table Builder

    Creates PostgreSQL tables directly from uploaded
    datasets without predefined schemas.
    """

    RESERVED_WORDS = {

        "user",
        "table",
        "group",
        "select",
        "where",
        "join",
        "order",
        "from",
        "by",
        "insert",
        "delete",
        "update",
        "create",
        "drop",
        "index",
        "constraint",

    }

    MAX_IDENTIFIER_LENGTH = 63

    def __init__(

        self,

        db: Session,

    ):

        self.db = db

        self.engine = db.get_bind()

        self.metadata = MetaData()

        self.inspector = inspect(self.engine)
        
        # ---------------------------------------------------------
    # Identifier Sanitization
    # ---------------------------------------------------------

    def sanitize_identifier(

        self,

        value: str,

    ) -> str:

        """
        Convert any dataset column/table name into
        PostgreSQL safe identifier.
        """

        value = str(value)

        value = value.strip().lower()

        value = value.replace(" ", "_")

        value = value.replace("-", "_")

        value = value.replace("/", "_")

        value = re.sub(

            r"[^a-zA-Z0-9_]",

            "",

            value,

        )

        if value == "":

            value = "unnamed_column"

        if value[0].isdigit():

            value = f"col_{value}"

        if keyword.iskeyword(value):

            value += "_"

        if value in self.RESERVED_WORDS:

            value += "_"

        if len(value) > self.MAX_IDENTIFIER_LENGTH:

            value = value[: self.MAX_IDENTIFIER_LENGTH]

        return value
    
        # ---------------------------------------------------------

    def sanitize_columns(

        self,

        df: pd.DataFrame,

    ) -> pd.DataFrame:

        """
        Sanitize every column.
        """

        columns = []

        duplicates = {}

        for column in df.columns:

            name = self.sanitize_identifier(column)

            if name in duplicates:

                duplicates[name] += 1

                name = f"{name}_{duplicates[name]}"

            else:

                duplicates[name] = 1

            columns.append(name)

        df.columns = columns

        return df
        # ---------------------------------------------------------

    def sanitize_table_name(

        self,

        table_name: str,

    ) -> str:

        """
        Produce valid PostgreSQL table name.
        """

        return self.sanitize_identifier(table_name)
    
        # ---------------------------------------------------------

    def table_exists(

        self,

        table_name: str,

    ) -> bool:

        table_name = self.sanitize_table_name(table_name)

        return self.inspector.has_table(table_name)
    
        # ---------------------------------------------------------

    def existing_columns(

        self,

        table_name: str,

    ) -> List[str]:

        if not self.table_exists(table_name):

            return []

        columns = self.inspector.get_columns(table_name)

        return [

            column["name"]

            for column in columns

        ]
        # ---------------------------------------------------------
    # PostgreSQL Type Inference Engine
    # ---------------------------------------------------------

    def infer_sqlalchemy_type(self, series: pd.Series):
        """
        Infer the most appropriate SQLAlchemy type
        for a pandas Series.
        """

        dtype = series.dtype

        # Boolean
        if pd.api.types.is_bool_dtype(dtype):
            return Boolean

        # Integer
        if pd.api.types.is_integer_dtype(dtype):
            return self._infer_integer_type(series)

        # Float
        if pd.api.types.is_float_dtype(dtype):
            return Float

        # Decimal
        if self._is_decimal_series(series):
            return Numeric(18, 4)

        # Datetime
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return DateTime

        # Date
        if self._is_date_series(series):
            return Date

        # String
        if pd.api.types.is_string_dtype(dtype):
            return self._infer_string_type(series)

        # Category
        if pd.api.types.is_categorical_dtype(dtype):
            return String(255)

        # Fallback
        return Text
    
        # ---------------------------------------------------------

    def _infer_integer_type(self, series: pd.Series):
        """
        Choose Integer for now.
        Future:
            SmallInteger
            BigInteger
        """

        return Integer
    
        # ---------------------------------------------------------

    def _infer_string_type(self, series: pd.Series):

        """
        Automatically determine whether
        VARCHAR or TEXT should be used.
        """

        try:

            max_length = (

                series.fillna("")
                .astype(str)
                .str.len()
                .max()

            )

        except Exception:

            return Text

        if max_length is None:

            return String(255)

        # Short values

        if max_length <= 50:

            return String(50)

        if max_length <= 100:

            return String(100)

        if max_length <= 255:

            return String(255)

        if max_length <= 500:

            return String(500)

        if max_length <= 1000:

            return String(1000)

        return Text
    
        # ---------------------------------------------------------

    def _is_decimal_series(

        self,

        series: pd.Series,

    ) -> bool:

        """
        Detect Decimal objects.
        """

        for value in series.dropna():

            if isinstance(value, Decimal):

                return True

        return False
    
        # ---------------------------------------------------------

    def _is_date_series(

        self,

        series: pd.Series,

    ) -> bool:

        """
        Detect Python date objects.
        """

        for value in series.dropna().head(20):

            if isinstance(value, date):

                return True

        return False
    
        # ---------------------------------------------------------

    def is_uuid_column(

        self,

        series: pd.Series,

    ) -> bool:

        """
        Detect UUID formatted strings.

        Reserved for future enhancement.
        """

        pattern = re.compile(

            r"^[a-f0-9]{8}-"
            r"[a-f0-9]{4}-"
            r"[a-f0-9]{4}-"
            r"[a-f0-9]{4}-"
            r"[a-f0-9]{12}$",

            re.I,

        )

        sample = series.dropna().astype(str).head(20)

        if sample.empty:

            return False

        return all(pattern.match(value) for value in sample)
    
        # ---------------------------------------------------------

    def infer_schema(

        self,

        df: pd.DataFrame,

    ) -> Dict[str, object]:

        """
        Build schema definition.

        Example

        {
            "customer_id": Integer,
            "name": String(255),
            "amount": Float
        }
        """

        schema = {}

        for column in df.columns:

            schema[column] = self.infer_sqlalchemy_type(
                df[column]
            )

        return schema
    
        # ---------------------------------------------------------

    def schema_summary(

        self,

        df: pd.DataFrame,

    ) -> Dict:

        schema = self.infer_schema(df)

        return {

            column: str(sql_type)

            for column, sql_type in schema.items()

        }
        
        # ---------------------------------------------------------

    # ---------------------------------------------------------

    def create_column(

        self,

        column_name: str,

        column_type,

        nullable: bool = True,

    ) -> Column:

        """
        Build one SQLAlchemy column.
        """

        return Column(

            self.sanitize_identifier(column_name),

            column_type,

            nullable=nullable,

        )
        
        # ---------------------------------------------------------

    def system_columns(self) -> List[Column]:
        """
        Enterprise Design

        Uploaded datasets remain identical
        to source data.

        Metadata belongs in dataset_registry
        and upload_audit tables.
        """

        return []
        
        # ---------------------------------------------------------
        
    def build_columns(
        self,
        df: pd.DataFrame,
    ) -> List[Column]:

        columns: List[Column] = []

        # Detect natural primary key
        pk = self.detect_primary_key(df)

        # Add surrogate key only if needed
        if pk is None:
            columns.append(
                Column(
                    "id",
                    Integer,
                    primary_key=True,
                    autoincrement=True,
                )
            )

        schema = self.infer_schema(df)

        for column_name, column_type in schema.items():

            columns.append(
                self.create_column(
                    column_name,
                    column_type,
                    nullable=True,
                )
            )

        columns.extend(
            self.system_columns()
        )

        return columns
    def ensure_unique_columns(

        self,

        columns: List[Column],

    ) -> List[Column]:

        """
        Prevent duplicate SQLAlchemy columns.
        """

        unique = {}

        results = []

        for column in columns:

            if column.name not in unique:

                unique[column.name] = True

                results.append(column)

        return results

        # ---------------------------------------------------------

    def is_system_column(

        self,

        column_name: str,

    ) -> bool:

        return column_name in {

            "id",

            "upload_batch_id",

            "source_dataset",

            "created_at",

            "updated_at",

        }
        
        # ---------------------------------------------------------

    def detect_primary_key(

        self,

        df: pd.DataFrame,

    ) -> Optional[str]:

        """
        Attempt to identify a likely primary key.
        """

        candidates = [

            "id",

            "customer_id",

            "account_id",

            "transaction_id",

            "employee_id",

            "vendor_id",

        ]

        for column in df.columns:

            if column.lower() in candidates:

                return column

        return None

        # ---------------------------------------------------------

    def apply_primary_key(

        self,

        columns: List[Column],

        primary_key: Optional[str],

    ):

        """
        Replace autogenerated id if
        uploaded dataset already contains
        a reliable identifier.
        """

        if primary_key is None:

            return columns

        for column in columns:

            if column.name == primary_key:

                column.primary_key = True

                column.autoincrement = False

        return columns
        # ---------------------------------------------------------

   
    def generate_columns(

        self,

        df: pd.DataFrame,

    ) -> List[Column]:

        """
        Complete enterprise column builder.
        """

        df = self.sanitize_columns(df)

        columns = self.build_columns(df)

        columns = self.ensure_unique_columns(columns)

        pk = self.detect_primary_key(df)

        columns = self.apply_primary_key(

            columns,

            pk,

        )

        return columns

    # ---------------------------------------------------------
    # Dynamic Table Builder
    # ---------------------------------------------------------

    def build_table(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Table:
        """
        Build SQLAlchemy Table object dynamically.
        """

        table_name = self.sanitize_table_name(table_name)

        columns = self.generate_columns(df)

        table = Table(
            table_name,
            self.metadata,
            *columns,
            *self.build_unique_constraints_placeholder(
                columns,
                table_name,
            ),
            extend_existing=True,
        )

        return table
    # ---------------------------------------------------------

    def create_table(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Table:
        """
        Create PostgreSQL table dynamically.
        """

        table_name = self.sanitize_table_name(table_name)

        # <-- ADD HERE
        self.validate_table_name(table_name)
        self.validate_dataframe(df)

        logger.info(
            "Creating table '%s'",
            table_name,
        )

        table = self.build_table(
            table_name,
            df,
        )

        try:

            table.create(
                bind=self.engine,
                checkfirst=True,
            )

            self.create_indexes(table)

            logger.info(
                "Table '%s' created successfully.",
                table_name,
            )

        except SQLAlchemyError as ex:

            logger.exception(ex)

            raise

        return table
    # ---------------------------------------------------------

    def drop_table(
        self,
        table_name: str,
    ):
        """
        Drop PostgreSQL table.
        """

        table_name = self.sanitize_table_name(table_name)

        if not self.table_exists(table_name):
            return

        table = Table(
            table_name,
            self.metadata,
            autoload_with=self.engine,
        )

        table.drop(
            bind=self.engine,
            checkfirst=True,
        )

        logger.info(
            "Dropped table %s",
            table_name,
        )
        
    # ---------------------------------------------------------

    def load_table(
        self,
        table_name: str,
    ) -> Table:
        """
        Load existing PostgreSQL table.
        """

        return Table(
            self.sanitize_table_name(table_name),
            self.metadata,
            autoload_with=self.engine,
        )
        
    # ---------------------------------------------------------

    def create_if_not_exists(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Table:
        """
        Create table only if it doesn't exist.
        """

        if self.table_exists(table_name):

            logger.info(
                "Table already exists: %s",
                table_name,
            )

            return self.load_table(table_name)

        return self.create_table(
            table_name,
            df,
        )

    # ---------------------------------------------------------

    def refresh_metadata(self):
        """
        Refresh SQLAlchemy metadata.
        """

        self.metadata.clear()

        self.inspector = inspect(
            self.engine
        )
        
    # ---------------------------------------------------------

    def list_tables(self):
        """
        List all PostgreSQL tables.
        """

        return self.inspector.get_table_names()

    # ---------------------------------------------------------

    def describe_table(
        self,
        table_name: str,
    ):
        """
        Return table structure.
        """

        table_name = self.sanitize_table_name(
            table_name
        )

        return self.inspector.get_columns(
            table_name
        )
    # ---------------------------------------------------------

    def drop_all_dynamic_tables(self):

        for table in self.list_tables():

            if table.startswith("pg_"):
                continue

            if table.startswith("sql_"):
                continue

            self.drop_table(table)
            
        # ---------------------------------------------------------
    # Schema Evolution Engine
    # ---------------------------------------------------------

    def compare_schema(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> Dict:
        """
        Compare uploaded dataframe schema with
        existing PostgreSQL table.
        """

        uploaded = set(df.columns)

        existing = set(
            self.existing_columns(table_name)
        )

        return {

            "new_columns":
                sorted(uploaded - existing),

            "removed_columns":
                sorted(existing - uploaded),

            "common_columns":
                sorted(uploaded & existing),

        }
    
    def schema_changed(
        self,
        table_name: str,
        df: pd.DataFrame,
    ) -> bool:

        comparison = self.compare_schema(
            table_name,
            df,
        )

        return len(
            comparison["new_columns"]
        ) > 0
    
    def generate_alter_statements(
        self,
        table_name: str,
        df: pd.DataFrame,
    ):

        comparison = self.compare_schema(
            table_name,
            df,
        )

        schema = self.infer_schema(df)

        statements = []

        for column in comparison["new_columns"]:

            sql_type = schema[column]

            sql = (

                f'ALTER TABLE "{table_name}" '

                f'ADD COLUMN "{column}" '

                f'{self.sql_type(sql_type)}'

            )

            statements.append(sql)

        return statements
    
    def sql_type(
        self,
        column_type,
    ):

        if column_type == Integer:
            return "INTEGER"

        if column_type == Float:
            return "DOUBLE PRECISION"

        if column_type == Boolean:
            return "BOOLEAN"

        if column_type == Date:
            return "DATE"

        if column_type == DateTime:
            return "TIMESTAMP"

        if isinstance(column_type, Numeric):
            return "NUMERIC(18,4)"

        if isinstance(column_type, String):
            return f"VARCHAR({column_type.length})"

        return "TEXT"

    def evolve_schema(
        self,
        table_name: str,
        df: pd.DataFrame,
    ):

        if not self.schema_changed(
            table_name,
            df,
        ):
            logger.info(
                "Schema unchanged."
            )
            return

        statements = self.generate_alter_statements(
            table_name,
            df,
        )

        connection = self.engine.connect()

        try:

            transaction = connection.begin()

            for sql in statements:

                logger.info(sql)

                connection.execute(
                    text(sql)
                )

            transaction.commit()

        except Exception:

            transaction.rollback()

            raise

        finally:

            connection.close()

        self.refresh_metadata()
        
    def create_or_evolve(
        self,
        table_name: str,
        df: pd.DataFrame,
    ):

        if not self.table_exists(table_name):

            return self.create_table(
                table_name,
                df,
            )

        self.evolve_schema(
            table_name,
            df,
        )

        return self.load_table(
            table_name,
        )
        
    # ---------------------------------------------------------
    # Enterprise Index Manager
    # ---------------------------------------------------------

    def should_index(self, column_name: str) -> bool:
        """
        Determine if a column should receive an index.
        """

        column_name = column_name.lower()

        keywords = (
            "id",
            "customer",
            "account",
            "transaction",
            "email",
            "phone",
            "passport",
            "tax",
            "pan",
            "aadhaar",
            "swift",
            "iban",
            "company",
            "vendor",
            "employee",
            "country",
            "city",
            "branch",
            "date",
        )

        return any(keyword in column_name for keyword in keywords)
    
    def build_indexes(
        self,
        table: Table,
    ) -> List[Index]:
        """
        Create SQLAlchemy Index objects.
        """

        indexes = []

        for column in table.columns:

            if self.should_index(column.name):

                index_name = f"idx_{table.name}_{column.name}"

                indexes.append(
                    Index(
                        index_name,
                        column,
                    )
                )

        return indexes
    
    def create_indexes(
        self,
        table: Table,
    ):
        """
        Create indexes after table creation.
        """

        indexes = self.build_indexes(table)

        for index in indexes:

            try:

                index.create(
                    bind=self.engine,
                    checkfirst=True,
                )

                logger.info(
                    "Created index %s",
                    index.name,
                )

            except Exception as ex:

                logger.warning(
                    "Index creation failed: %s",
                    ex,
                )

    def should_be_unique(
        self,
        column_name: str,
    ) -> bool:

        names = {

            "customer_id",
            "account_id",
            "transaction_id",
            "employee_id",
            "vendor_id",

        }

        return column_name.lower() in names
    
    def build_unique_constraints(
        self,
        table: Table,
    ):

        constraints = []

        for column in table.columns:

            if self.should_be_unique(column.name):

                constraints.append(

                    UniqueConstraint(

                        column.name,

                        name=f"uq_{table.name}_{column.name}",

                    )

                )

        return constraints
    
    def build_unique_constraints_placeholder(
        self,
        columns: List[Column],
        table_name: str,
    ):
        """
        Build unique constraints before table creation.
        """

        constraints = []

        for column in columns:

            if self.should_be_unique(column.name):

                constraints.append(

                    UniqueConstraint(

                        column.name,

                        name=f"uq_{table_name}_{column.name}",

                    )

                )

        return constraints
    
    # ---------------------------------------------------------
    # Transaction Manager
    # ---------------------------------------------------------

    from contextlib import contextmanager

    @contextmanager
    def transaction(self):
        """
        Enterprise transaction manager.
        """

        connection = self.engine.connect()
        transaction = connection.begin()

        try:

            yield connection

            transaction.commit()

        except Exception:

            transaction.rollback()

            raise

        finally:

            connection.close()
            
    def execute_sql(
        self,
        sql: str,
    ):
        """
        Execute raw SQL safely.
        """

        with self.transaction() as connection:

            connection.execute(
                text(sql)
            )
            
    def execute_batch_sql(
        self,
        statements: List[str],
    ):

        with self.transaction() as connection:

            for sql in statements:

                logger.info(sql)

                connection.execute(
                    text(sql)
                )
                
    def validate_table_name(
        self,
        table_name: str,
    ):

        if not table_name:

            raise ValueError(
                "Table name cannot be empty."
            )

        if len(table_name) > 63:

            raise ValueError(
                "PostgreSQL table name too long."
            )
            
            
    def validate_dataframe(
        self,
        df: pd.DataFrame,
    ):

        if df.empty:

            raise ValueError(
                "Uploaded dataframe is empty."
            )

        if len(df.columns) == 0:

            raise ValueError(
                "Dataset contains no columns."
            )
    
    def retry_create_table(
        self,
        table_name: str,
        df: pd.DataFrame,
        retries: int = 3,
    ):

        for attempt in range(retries):

            try:

                return self.create_table(
                    table_name,
                    df,
                )

            except Exception as ex:

                logger.warning(

                    "Retry %s failed: %s",

                    attempt + 1,

                    ex,

                )

                time.sleep(2)

        raise RuntimeError(
            "Unable to create table."
        )
        
        
    def prepare_dataframe(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare dataframe before bulk load.
        """

        df = df.copy()

        df = self.sanitize_columns(df)

        df = df.replace(
            {np.nan: None}
        )

        return df
            
            
    def statistics(
        self,
        df: pd.DataFrame,
    ):

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "memory_mb": round(

                df.memory_usage(
                    deep=True
                ).sum()
                / 1024 / 1024,

                2,

            ),

        }
    
    def health_check(self):

        return {

            "database":

                str(self.engine.url),

            "tables":

                len(self.list_tables()),

            "connected":

                True,

        }
        
    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def table_metadata(
        self,
        table_name: str,
    ) -> Dict:
        """
        Return PostgreSQL table metadata.
        """

        table_name = self.sanitize_table_name(table_name)

        if not self.table_exists(table_name):
            raise ValueError(
                f"Table '{table_name}' does not exist."
            )

        columns = self.inspector.get_columns(table_name)

        indexes = self.inspector.get_indexes(table_name)

        pk = self.inspector.get_pk_constraint(table_name)

        return {

            "table": table_name,

            "columns": columns,

            "indexes": indexes,

            "primary_key": pk,

        }
        
    def drop_tables(
        self,
        tables: List[str],
    ):
        """
        Drop multiple tables.
        """

        for table in tables:

            try:

                self.drop_table(table)

            except Exception as ex:

                logger.warning(ex)
                
    def rename_table(
        self,
        old_name: str,
        new_name: str,
    ):
        """
        Rename PostgreSQL table.
        """

        old_name = self.sanitize_table_name(old_name)

        new_name = self.sanitize_table_name(new_name)

        sql = (

            f'ALTER TABLE "{old_name}" '

            f'RENAME TO "{new_name}"'

        )

        self.execute_sql(sql)

        self.refresh_metadata()
        
        
    def copy_table(
        self,
        source: str,
        target: str,
    ):
        """
        Create table copy.
        """

        source = self.sanitize_table_name(source)

        target = self.sanitize_table_name(target)

        sql = (

            f'CREATE TABLE "{target}" '

            f'AS TABLE "{source}"'

        )

        self.execute_sql(sql)
        
    def database_summary(self):

        tables = self.list_tables()

        return {

            "total_tables": len(tables),

            "tables": tables,

        }