"""
==========================================================
AML Investigation Platform

Date Validator

Responsibilities
----------------
✓ Validate date values
✓ Support multiple date formats

==========================================================
"""

from __future__ import annotations

from datetime import datetime

from app.core.column_patterns import DATE_PATTERNS
from app.validators.pattern_validator import PatternValidator


class DateValidator(PatternValidator):
    """
    Validates date columns.
    """

    name = "Date Validator"

    priority = 30

    supported_columns = DATE_PATTERNS

    DATE_FORMATS = [

        "%Y-%m-%d",

        "%d-%m-%Y",

        "%m-%d-%Y",

        "%d/%m/%Y",

        "%m/%d/%Y",

        "%Y/%m/%d",

        "%Y%m%d",
    ]

    def is_valid(
        self,
        value: str,
    ) -> bool:

        if value is None:
            return False

        value = value.strip()

        if value == "":
            return False

        for fmt in self.DATE_FORMATS:

            try:

                datetime.strptime(value, fmt)

                return True

            except ValueError:

                continue

        return False