"""
==========================================================
AML Investigation Platform

Validation Service

Responsibilities
----------------
✓ Validate uploaded datasets
✓ Validate schema
✓ Validate dataframe
✓ Validate data quality
✓ Produce validation report

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from app.core.exceptions import (
    DatasetValidationError,
)
from app.utils.validation_utils import (
    duplicate_percentage,
    missing_percentage,
    validate_columns,
    validate_dataframe,
)


# ==========================================================
# Validation Report
# ==========================================================

@dataclass
class ValidationReport:

    is_valid: bool = True

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    statistics: dict = field(default_factory=dict)


# ==========================================================
# Validation Service
# ==========================================================

class ValidationService:

    """
    Dataset validation engine.
    """

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> ValidationReport:

        report = ValidationReport()

        try:

            validate_dataframe(dataframe)

            validate_columns(dataframe)

        except DatasetValidationError as exc:

            report.is_valid = False

            report.errors.append(str(exc))

            return report

        except Exception as exc:

            report.is_valid = False

            report.errors.append(str(exc))

            return report

        # -----------------------------------------------
        # Missing Values
        # -----------------------------------------------

        missing = missing_percentage(dataframe)

        report.statistics["missing_percentage"] = missing

        if missing > 40:

            report.warnings.append(
                f"High missing values ({missing}%)."
            )

        # -----------------------------------------------
        # Duplicate Rows
        # -----------------------------------------------

        duplicates = duplicate_percentage(dataframe)

        report.statistics["duplicate_percentage"] = duplicates

        if duplicates > 25:

            report.warnings.append(
                f"High duplicate percentage ({duplicates}%)."
            )

        # -----------------------------------------------
        # Rows / Columns
        # -----------------------------------------------

        report.statistics["rows"] = len(dataframe)

        report.statistics["columns"] = len(dataframe.columns)

        return report