"""
==========================================================
AML Investigation Platform

Currency Validator

Responsibilities
----------------
✓ Validate ISO currency codes
✓ Detect invalid currencies

==========================================================
"""

from __future__ import annotations

from app.core.column_patterns import CURRENCY_PATTERNS
from app.validators.pattern_validator import PatternValidator


class CurrencyValidator(PatternValidator):
    """
    Validates currency columns.
    """

    name = "Currency Validator"

    priority = 50

    supported_columns = CURRENCY_PATTERNS

    VALID_CURRENCIES = {
        "USD",
        "EUR",
        "GBP",
        "INR",
        "JPY",
        "AUD",
        "CAD",
        "CHF",
        "CNY",
        "SGD",
        "AED",
        "SAR",
        "HKD",
        "NZD",
        "SEK",
        "NOK",
        "DKK",
        "ZAR",
        "BRL",
        "MXN",
    }

    def is_valid(
        self,
        value: str,
    ) -> bool:

        if value is None:
            return False

        value = value.strip().upper()

        if value == "":
            return False

        return value in self.VALID_CURRENCIES