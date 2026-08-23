"""
==========================================================
AML Investigation Platform

Enterprise Dataset Profiler

Responsibilities
----------------
✓ Dataset statistics
✓ Column profiling
✓ Candidate key detection
✓ Data quality metrics
✓ PII detection
✓ AML identifier detection
✓ Numeric statistics
✓ Dashboard metadata
✓ Entity Resolution support

==========================================================
"""

from __future__ import annotations

import logging
import re

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DatasetProfiler:
    """
    Enterprise Dataset Profiler.

    Generates dataset metadata used by:

    - Dashboard
    - Upload Summary
    - Entity Resolution
    - AI Copilot
    - Investigation Engine
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_PATTERN = re.compile(
        r"^[0-9+\-\s()]{7,20}$"
    )

    SAMPLE_SIZE = 100

    def __init__(self):
        logger.info("DatasetProfiler initialized.")
        
    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _validate_dataframe(
        self,
        df: Optional[pd.DataFrame],
    ) -> None:
        """
        Validate dataframe input.
        """

        if df is None:
            raise ValueError("DataFrame cannot be None.")

    def _sample(
        self,
        series: pd.Series,
    ) -> pd.Series:
        """
        Return a representative sample
        from a dataframe column.
        """

        return (
            series
            .dropna()
            .astype(str)
            .head(self.SAMPLE_SIZE)
        )

    def _safe_round(
        self,
        value: Any,
        digits: int = 2,
    ):
        """
        Safely round numeric values.
        """

        try:
            return round(float(value), digits)

        except Exception:
            return None
    # ---------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------

    def summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Overall dataset statistics.
        """

        self._validate_dataframe(df)

        logger.info("Generating dataset summary.")

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "memory_mb": self._safe_round(

                df.memory_usage(
                    deep=True
                ).sum() / 1024 / 1024

            ),

            "duplicate_rows": int(

                df.duplicated().sum()

            ),

            "duplicate_percent": self._safe_round(

                df.duplicated().mean() * 100

            ),

        }
        
    # ---------------------------------------------------------
    # Null Summary
    # ---------------------------------------------------------

    def null_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate null statistics.
        """

        self._validate_dataframe(df)

        logger.info("Calculating null summary.")

        results = {}

        total_rows = len(df)

        for column in df.columns:

            nulls = int(
                df[column].isna().sum()
            )

            results[column] = {

                "null_count": nulls,

                "null_percent": self._safe_round(

                    (
                        nulls / total_rows * 100
                    )

                    if total_rows

                    else 0

                ),

            }

        return results
    
    # ---------------------------------------------------------
    # Unique Values
    # ---------------------------------------------------------

    def unique_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze unique values.
        """

        self._validate_dataframe(df)

        logger.info("Calculating unique statistics.")

        results = {}

        total_rows = len(df)

        for column in df.columns:

            unique_count = int(

                df[column].nunique(
                    dropna=True
                )

            )

            results[column] = {

                "unique_count": unique_count,

                "duplicate_count": max(
                    0,
                    total_rows - unique_count,
                ),

                "is_unique": bool(
                    df[column].is_unique
                ),

            }

        return results
    
    # ---------------------------------------------------------
    # Candidate Keys
    # ---------------------------------------------------------

    def candidate_keys(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Identify columns that
        can act as primary keys.
        """

        self._validate_dataframe(df)

        logger.info(
            "Finding candidate keys."
        )

        keys = []

        for column in df.columns:

            if (

                df[column].notna().all()

                and

                df[column].is_unique

            ):

                keys.append(column)

        return keys
    
    # ---------------------------------------------------------
    # Column Types
    # ---------------------------------------------------------

    def column_types(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:
        """
        Return pandas dtypes.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting column types."
        )

        return {

            column: str(
                df[column].dtype
            )

            for column in df.columns

        }
        
    # ---------------------------------------------------------
    # Email Detection
    # ---------------------------------------------------------

    def detect_email_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect email columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting email columns."
        )

        columns = []

        for column in df.columns:

            sample = self._sample(
                df[column]
            )

            if sample.empty:
                continue

            matches = sum(
                bool(
                    self.EMAIL_PATTERN.match(
                        value
                    )
                )
                for value in sample
            )

            if matches >= max(
                1,
                int(len(sample) * 0.8),
            ):
                columns.append(column)

        return columns
    
    # ---------------------------------------------------------
    # Phone Detection
    # ---------------------------------------------------------

    def detect_phone_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect phone number columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting phone columns."
        )

        columns = []

        for column in df.columns:

            sample = self._sample(
                df[column]
            )

            if sample.empty:
                continue

            matches = sum(
                bool(
                    self.PHONE_PATTERN.match(
                        value
                    )
                )
                for value in sample
            )

            if matches >= max(
                1,
                int(len(sample) * 0.8),
            ):
                columns.append(column)

        return columns
    
    # ---------------------------------------------------------
    # AML Identifier Detection
    # ---------------------------------------------------------

    def identifier_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect AML identifier columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting identifier columns."
        )

        keywords = {

            "id",

            "customer",

            "customer_id",

            "client",

            "client_id",

            "account",

            "account_id",

            "transaction",

            "txn",

            "employee",

            "vendor",

            "merchant",

            "beneficiary",

            "company",

            "passport",

            "pan",

            "aadhaar",

            "tax",

            "tin",

            "ifsc",

            "swift",

            "bic",

            "iban",

            "wallet",

            "email",

            "phone",

        }

        identifiers = []

        for column in df.columns:

            name = column.lower()

            if any(
                keyword in name
                for keyword in keywords
            ):
                identifiers.append(column)

        return identifiers
    
    # ---------------------------------------------------------
    # Date Detection
    # ---------------------------------------------------------

    def detect_date_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect date columns.
        """

        self._validate_dataframe(df)

        logger.info(
            "Detecting date columns."
        )

        dates = []

        for column in df.columns:

            if pd.api.types.is_datetime64_any_dtype(
                df[column]
            ):

                dates.append(column)

                continue

            sample = (
                df[column]
                .dropna()
                .head(self.SAMPLE_SIZE)
            )

            if sample.empty:
                continue

            try:

                converted = pd.to_datetime(
                    sample,
                    errors="coerce",
                )

                if converted.notna().mean() >= 0.8:

                    dates.append(column)

            except Exception:

                continue

        return dates
    
    # ---------------------------------------------------------
    # Numeric Statistics
    # ---------------------------------------------------------

    def numeric_statistics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Numeric statistics.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating numeric statistics."
        )

        statistics = {}

        numeric = df.select_dtypes(
            include="number"
        )

        for column in numeric.columns:

            series = numeric[column]

            statistics[column] = {

                "count": int(
                    series.count()
                ),

                "min": self._safe_round(
                    series.min()
                ),

                "max": self._safe_round(
                    series.max()
                ),

                "mean": self._safe_round(
                    series.mean()
                ),

                "median": self._safe_round(
                    series.median()
                ),

                "std": self._safe_round(
                    series.std()
                ),

                "sum": self._safe_round(
                    series.sum()
                ),

            }

        return statistics
    
    # ---------------------------------------------------------
    # Column Classification
    # ---------------------------------------------------------

    def classify_columns(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:
        """
        Classify each column by purpose.
        """

        self._validate_dataframe(df)

        logger.info(
            "Classifying columns."
        )

        emails = set(
            self.detect_email_columns(df)
        )

        phones = set(
            self.detect_phone_columns(df)
        )

        dates = set(
            self.detect_date_columns(df)
        )

        identifiers = set(
            self.identifier_columns(df)
        )

        classification = {}

        for column in df.columns:

            if column in identifiers:

                classification[column] = "IDENTIFIER"

            elif column in emails:

                classification[column] = "EMAIL"

            elif column in phones:

                classification[column] = "PHONE"

            elif column in dates:

                classification[column] = "DATE"

            elif pd.api.types.is_numeric_dtype(
                df[column]
            ):

                classification[column] = "NUMERIC"

            else:

                classification[column] = "TEXT"

        return classification
    
        # ---------------------------------------------------------
    # Dataset Metrics
    # ---------------------------------------------------------

    def dataset_metrics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Overall dataset metrics.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating dataset metrics."
        )

        return {

            "total_cells": int(df.size),

            "total_nulls": int(
                df.isna().sum().sum()
            ),

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "duplicate_percent": self._safe_round(
                df.duplicated().mean() * 100
            ),

            "memory_mb": self._safe_round(
                df.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024
            ),

        }
        
        # ---------------------------------------------------------
    # Data Quality Score
    # ---------------------------------------------------------

    def quality_score(
        self,
        df: pd.DataFrame,
    ) -> float:
        """
        Calculate an overall quality score.
        """

        self._validate_dataframe(df)

        logger.info(
            "Calculating quality score."
        )

        if df.empty:
            return 0.0

        total_cells = df.size

        if total_cells == 0:
            return 0.0

        null_ratio = (

            df.isna()
            .sum()
            .sum()

            / total_cells

        )

        duplicate_ratio = (

            df.duplicated()
            .mean()

        )

        score = (

            100

            - (null_ratio * 50)

            - (duplicate_ratio * 50)

        )

        return round(
            max(score, 0),
            2,
        )
        
        # ---------------------------------------------------------
    # Complete Profile
    # ---------------------------------------------------------

    def profile(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate a complete dataset profile.
        """

        self._validate_dataframe(df)

        logger.info(
            "Generating complete dataset profile."
        )

        try:

            profile = {

                "summary":
                    self.summary(df),

                "metrics":
                    self.dataset_metrics(df),

                "null_summary":
                    self.null_summary(df),

                "unique_summary":
                    self.unique_summary(df),

                "candidate_keys":
                    self.candidate_keys(df),

                "column_types":
                    self.column_types(df),

                "column_classification":
                    self.classify_columns(df),

                "email_columns":
                    self.detect_email_columns(df),

                "phone_columns":
                    self.detect_phone_columns(df),

                "identifier_columns":
                    self.identifier_columns(df),

                "date_columns":
                    self.detect_date_columns(df),

                "numeric_statistics":
                    self.numeric_statistics(df),

                "quality_score":
                    self.quality_score(df),

            }

            logger.info(
                "Dataset profiling completed successfully."
            )

            return profile

        except Exception as ex:

            logger.exception(
                "Dataset profiling failed."
            )

            raise RuntimeError(
                f"Dataset profiling failed: {str(ex)}"
            ) from ex
        # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self) -> Dict[str, str]:
        """
        Health status.
        """

        return {

            "service": "DatasetProfiler",

            "status": "healthy",

        }