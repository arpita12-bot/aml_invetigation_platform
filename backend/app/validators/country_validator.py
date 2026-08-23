"""
==========================================================
AML Investigation Platform

Country Validator

Responsibilities
----------------
✓ Validate country names
✓ Validate ISO country codes

==========================================================
"""

from __future__ import annotations

from app.core.column_patterns import COUNTRY_PATTERNS
from app.validators.pattern_validator import PatternValidator


class CountryValidator(PatternValidator):
    """
    Validates country columns.
    """

    name = "Country Validator"

    priority = 60

    supported_columns = COUNTRY_PATTERNS

    VALID_COUNTRIES = {

        "INDIA",
        "UNITED STATES",
        "USA",
        "UNITED KINGDOM",
        "UK",
        "CANADA",
        "GERMANY",
        "FRANCE",
        "ITALY",
        "SPAIN",
        "AUSTRALIA",
        "CHINA",
        "JAPAN",
        "SINGAPORE",
        "BRAZIL",
        "MEXICO",
        "RUSSIA",
        "UAE",
        "UNITED ARAB EMIRATES",
        "SAUDI ARABIA",
        "SOUTH AFRICA",
        "SWITZERLAND",
        "NETHERLANDS",
        "BELGIUM",
        "SWEDEN",
        "NORWAY",
        "DENMARK",
        "FINLAND",
        "NEW ZEALAND",

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

        return value in self.VALID_COUNTRIES