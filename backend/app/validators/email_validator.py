"""
==========================================================
AML Investigation Platform

Email Validator

Responsibilities
----------------
✓ Validate email addresses
✓ Detect invalid email formats

==========================================================
"""

from __future__ import annotations

import re

from app.core.column_patterns import EMAIL_PATTERNS
from app.validators.pattern_validator import PatternValidator


class EmailValidator(PatternValidator):
    """
    Validates email address columns.
    """

    name = "Email Validator"

    priority = 10

    supported_columns = EMAIL_PATTERNS

    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
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
            self.EMAIL_REGEX.fullmatch(value)
        )