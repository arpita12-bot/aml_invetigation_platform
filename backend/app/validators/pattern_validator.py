"""
==========================================================
AML Investigation Platform

Pattern Validator

Responsibilities
----------------
✓ Generic validator for pattern-based columns
✓ Handles all common validation logic
✓ Used by Email, Phone, Date, Currency,
  Country and Amount validators

==========================================================
"""

from __future__ import annotations

from abc import abstractmethod

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class PatternValidator(BaseValidator):
    """
    Base class for all pattern-based validators.

    Child validators only need to implement
    is_valid(value).

    Everything else is handled automatically.
    """

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        columns = self.matching_columns(detected_columns)

        if not columns:
            self.add_warning(
                result,
                f"No supported columns found for {self.name}."
            )
            return result

        total_values = 0
        invalid_values = 0
        duplicate_values = 0

        for column in columns:

            series = dataframe[column]

            # Remove nulls
            values = (
                series.dropna()
                .astype(str)
                .str.strip()
            )

            total_values += len(values)

            duplicate_values += (
                values.duplicated().sum()
            )

            invalid = values[
                ~values.apply(self.is_valid)
            ]

            invalid_values += len(invalid)

            if len(invalid) > 0:

                self.add_warning(
                    result,
                    f"{column}: {len(invalid)} invalid values found."
                )

        self.add_statistic(
            result,
            "columns_checked",
            len(columns),
        )

        self.add_statistic(
            result,
            "values_checked",
            total_values,
        )

        self.add_statistic(
            result,
            "invalid_values",
            invalid_values,
        )

        self.add_statistic(
            result,
            "duplicate_values",
            duplicate_values,
        )

        if invalid_values > 0:

            result.passed = False

        return result

    # -------------------------------------------------
    # Child validator implementation
    # -------------------------------------------------

    @abstractmethod
    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Child validator implements only this method.
        """
        pass