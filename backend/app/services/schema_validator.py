"""
==========================================================
AML Investigation Platform

Schema Validator

Responsibilities
----------------
✓ Validate uploaded datasets
✓ Validate schema integrity
✓ Validate column names
✓ Validate dataset size
✓ Generate validation report

==========================================================
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd


class SchemaValidator:

    MAX_COLUMNS = 500
    MAX_ROWS = 10_000_000

    VALID_COLUMN_TYPES = {
        "object",
        "int64",
        "float64",
        "bool",
        "datetime64[ns]",
        "category",
    }

    # ---------------------------------------------------------

    def validate(self, df: pd.DataFrame) -> Dict:

        errors = []
        warnings = []

        self._validate_empty(df, errors)
        self._validate_columns(df, errors)
        self._validate_duplicate_columns(df, errors)
        self._validate_column_names(df, errors)
        self._validate_column_count(df, errors)
        self._validate_row_count(df, errors)
        self._validate_dtypes(df, warnings)
        self._validate_duplicate_rows(df, warnings)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    # ---------------------------------------------------------

    def _validate_empty(self, df, errors):

        if df.empty:
            errors.append("Dataset is empty.")

    # ---------------------------------------------------------

    def _validate_columns(self, df, errors):

        if len(df.columns) == 0:
            errors.append("Dataset contains no columns.")

    # ---------------------------------------------------------

    def _validate_duplicate_columns(self, df, errors):

        duplicates = df.columns[df.columns.duplicated()].tolist()

        if duplicates:
            errors.append(
                f"Duplicate columns detected: {duplicates}"
            )

    # ---------------------------------------------------------

    def _validate_column_names(self, df, errors):

        invalid = []

        for col in df.columns:

            if col is None:
                invalid.append("None")

            elif str(col).strip() == "":
                invalid.append("Blank")

        if invalid:
            errors.append(
                f"Invalid column names: {invalid}"
            )

    # ---------------------------------------------------------

    def _validate_column_count(self, df, errors):

        if len(df.columns) > self.MAX_COLUMNS:

            errors.append(
                f"Maximum allowed columns: {self.MAX_COLUMNS}"
            )

    # ---------------------------------------------------------

    def _validate_row_count(self, df, errors):

        if len(df) > self.MAX_ROWS:

            errors.append(
                f"Maximum allowed rows: {self.MAX_ROWS}"
            )

    # ---------------------------------------------------------

    def _validate_dtypes(self, df, warnings):

        unsupported = []

        for col in df.columns:

            dtype = str(df[col].dtype)

            if dtype not in self.VALID_COLUMN_TYPES:

                unsupported.append(
                    f"{col} ({dtype})"
                )

        if unsupported:

            warnings.append(
                f"Unsupported data types detected: {unsupported}"
            )

    # ---------------------------------------------------------

    def _validate_duplicate_rows(self, df, warnings):

        duplicate_rows = df.duplicated().sum()

        if duplicate_rows > 0:

            warnings.append(
                f"{duplicate_rows} duplicate records detected."
            )