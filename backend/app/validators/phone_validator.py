"""
==========================================================
AML Investigation Platform

Phone Validator

Responsibilities
----------------
✓ Validate phone numbers
✓ Detect invalid phone formats

==========================================================
"""

from __future__ import annotations

import re

from app.core.column_patterns import PHONE_PATTERNS
from app.validators.pattern_validator import PatternValidator


class PhoneValidator(PatternValidator):
    """
    Validates phone number columns.
    """

    name = "Phone Validator"

    priority = 20

    supported_columns = PHONE_PATTERNS

    PHONE_REGEX = re.compile(
        r"^\+?[0-9][0-9\s\-\(\)]{7,20}$"
    )

    def is_valid(
        self,
        value: str,
    ) -> bool:

        if value is None:
            return False

        value = value.strip()

        if value == "":
            return False

        return bool(
            self.PHONE_REGEX.fullmatch(value)
        )