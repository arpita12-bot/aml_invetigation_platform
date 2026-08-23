"""
==========================================================
AML Investigation Platform

Amount Validator

Responsibilities
----------------
✓ Validate monetary amounts
✓ Detect invalid amount values

==========================================================
"""

from __future__ import annotations

import re

from app.core.column_patterns import AMOUNT_PATTERNS
from app.validators.pattern_validator import PatternValidator


class AmountValidator(PatternValidator):
    """
    Validates monetary amount columns.
    """

    name = "Amount Validator"

    priority = 40

    supported_columns = AMOUNT_PATTERNS

    AMOUNT_REGEX = re.compile(
        r"^-?\d+(\.\d{1,2})?$"
    )

    def is_valid(
        self,
        value: str,
    ) -> bool:

        if value is None:
            return False

        value = str(value).strip().replace(",", "")

        if value == "":
            return False

        if not self.AMOUNT_REGEX.fullmatch(value):
            return False

        try:
            float(value)
            return True
        except ValueError:
            return False