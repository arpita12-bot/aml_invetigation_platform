"""
==========================================================
AML Investigation Platform

Type Inference Service

Responsibilities
----------------
✓ Infer PostgreSQL data types
✓ Infer Neo4j property types
✓ Detect nullable columns
✓ Detect uniqueness
✓ Calculate profiling statistics
✓ Produce ColumnMetadata

==========================================================
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

from app.models.schema.column_metadata import (
    ColumnMetadata,
)


class TypeInferenceService:
    """
    Infers metadata for dataframe columns.
    """

    # -----------------------------------------
    # Public API
    # -----------------------------------------

    @classmethod
    def infer(
        cls,
        dataframe: pd.DataFrame,
    ) -> list[ColumnMetadata]:

        metadata = []

        for column in dataframe.columns:

            metadata.append(

                cls.infer_column(
                    dataframe,
                    column,
                )

            )

        return metadata

    # -----------------------------------------
    # Infer Single Column
    # -----------------------------------------

    @classmethod
    def infer_column(
        cls,
        dataframe: pd.DataFrame,
        column_name: str,
    ) -> ColumnMetadata:

        series = dataframe[column_name]

        sql_type = cls._infer_sql_type(series)

        return ColumnMetadata(

            name=column_name,

            original_name=column_name,

            sql_type=sql_type,

            nullable=series.isna().any(),

            unique=series.is_unique,

            max_length=cls._max_length(series),

            min_length=cls._min_length(series),

            distinct_count=series.nunique(),

            null_count=series.isna().sum(),

            duplicate_count=series.duplicated().sum(),

            minimum=cls._minimum(series),

            maximum=cls._maximum(series),

            mean=cls._mean(series),

            median=cls._median(series),

            std_dev=cls._std(series),

            sample_values=cls._sample_values(series),

        )

    # -----------------------------------------
    # SQL Type
    # -----------------------------------------

    @staticmethod
    def _infer_sql_type(
        series: pd.Series,
    ) -> str:

        if is_integer_dtype(series):

            return "BIGINT"

        if is_float_dtype(series):

            return "DOUBLE PRECISION"

        if is_bool_dtype(series):

            return "BOOLEAN"

        if is_datetime64_any_dtype(series):

            return "TIMESTAMP"

        # Try datetime conversion

        sample = series.dropna().head(50)

        if not sample.empty:

            converted = pd.to_datetime(
                sample,
                errors="coerce",
            )

            if converted.notna().mean() >= 0.90:
                return "TIMESTAMP"

        max_length = (

            series.fillna("")
            .astype(str)
            .str.len()
            .max()

        )

        if max_length <= 255:

            return f"VARCHAR({max_length})"

        return "TEXT"

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    @staticmethod
    def _max_length(series):

        if series.empty:

            return 0

        return (

            series.fillna("")
            .astype(str)
            .str.len()
            .max()

        )

    @staticmethod
    def _min_length(series):

        if series.empty:

            return 0

        values = (

            series.dropna()
            .astype(str)
            .str.len()

        )

        if values.empty:

            return 0

        return values.min()

    @staticmethod
    def _minimum(series):

        try:

            return series.min()

        except Exception:

            return None

    @staticmethod
    def _maximum(series):

        try:

            return series.max()

        except Exception:

            return None

    @staticmethod
    def _mean(series):

        try:

            return round(series.mean(), 4)

        except Exception:

            return None

    @staticmethod
    def _median(series):

        try:

            return series.median()

        except Exception:

            return None

    @staticmethod
    def _std(series):

        try:

            return round(series.std(), 4)

        except Exception:

            return None

    @staticmethod
    def _sample_values(
        series,
        limit: int = 5,
    ):

        return (

            series.dropna()
            .head(limit)
            .tolist()

        )