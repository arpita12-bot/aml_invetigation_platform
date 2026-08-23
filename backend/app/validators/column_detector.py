"""
==========================================================
AML Investigation Platform

Column Detector

Responsibilities
----------------
✓ Detect AML-related columns
✓ Support heterogeneous datasets
✓ Centralize column discovery
✓ Provide detected columns to validators

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.core.column_patterns import (
    ACCOUNT_PATTERNS,
    ACCOUNT_TYPE_PATTERNS,
    ADVERSE_NEWS_PATTERNS,
    AMOUNT_PATTERNS,
    BANK_PATTERNS,
    COMPANY_PATTERNS,
    COUNTRY_PATTERNS,
    CURRENCY_PATTERNS,
    CUSTOMER_NAME_PATTERNS,
    CUSTOMER_PATTERNS,
    DATE_PATTERNS,
    EMAIL_PATTERNS,
    FIRST_NAME_PATTERNS,
    LAST_NAME_PATTERNS,
    PEP_PATTERNS,
    PHONE_PATTERNS,
    RISK_LEVEL_PATTERNS,
    RISK_PATTERNS,
    RISK_SCORE_PATTERNS,
    SANCTION_PATTERNS,
    TAX_ID_PATTERNS,
    TRANSACTION_PATTERNS,
    WATCHLIST_PATTERNS,
)


# ==========================================================
# Detection Result
# ==========================================================


@dataclass
class DetectedColumns:

    email: list[str]

    phone: list[str]

    date: list[str]

    amount: list[str]

    currency: list[str]

    country: list[str]

    customer: list[str]

    customer_name: list[str]

    first_name: list[str]

    last_name: list[str]

    account: list[str]

    account_type: list[str]

    bank: list[str]

    company: list[str]

    tax_id: list[str]

    transaction: list[str]

    risk: list[str]

    risk_score: list[str]

    risk_level: list[str]

    pep: list[str]

    sanctions: list[str]

    watchlist: list[str]

    adverse_news: list[str]


# ==========================================================
# Column Detector
# ==========================================================


class ColumnDetector:
    """
    Detect AML-related columns from uploaded datasets.
    """

    @staticmethod
    def _find_columns(
        dataframe_columns: list[str],
        patterns: list[str],
    ) -> list[str]:

        matches = []

        for column in dataframe_columns:

            column_name = column.lower().strip()

            if any(
                pattern in column_name
                for pattern in patterns
            ):
                matches.append(column)

        return matches

    @classmethod
    def detect(
        cls,
        dataframe: pd.DataFrame,
    ) -> DetectedColumns:

        columns = list(dataframe.columns)

        return DetectedColumns(

            email=cls._find_columns(
                columns,
                EMAIL_PATTERNS,
            ),

            phone=cls._find_columns(
                columns,
                PHONE_PATTERNS,
            ),

            date=cls._find_columns(
                columns,
                DATE_PATTERNS,
            ),

            amount=cls._find_columns(
                columns,
                AMOUNT_PATTERNS,
            ),

            currency=cls._find_columns(
                columns,
                CURRENCY_PATTERNS,
            ),

            country=cls._find_columns(
                columns,
                COUNTRY_PATTERNS,
            ),

            customer=cls._find_columns(
                columns,
                CUSTOMER_PATTERNS,
            ),

            customer_name=cls._find_columns(
                columns,
                CUSTOMER_NAME_PATTERNS,
            ),

            first_name=cls._find_columns(
                columns,
                FIRST_NAME_PATTERNS,
            ),

            last_name=cls._find_columns(
                columns,
                LAST_NAME_PATTERNS,
            ),

            account=cls._find_columns(
                columns,
                ACCOUNT_PATTERNS,
            ),

            account_type=cls._find_columns(
                columns,
                ACCOUNT_TYPE_PATTERNS,
            ),

            bank=cls._find_columns(
                columns,
                BANK_PATTERNS,
            ),

            company=cls._find_columns(
                columns,
                COMPANY_PATTERNS,
            ),

            tax_id=cls._find_columns(
                columns,
                TAX_ID_PATTERNS,
            ),

            transaction=cls._find_columns(
                columns,
                TRANSACTION_PATTERNS,
            ),

            risk=cls._find_columns(
                columns,
                RISK_PATTERNS,
            ),

            risk_score=cls._find_columns(
                columns,
                RISK_SCORE_PATTERNS,
            ),

            risk_level=cls._find_columns(
                columns,
                RISK_LEVEL_PATTERNS,
            ),

            pep=cls._find_columns(
                columns,
                PEP_PATTERNS,
            ),

            sanctions=cls._find_columns(
                columns,
                SANCTION_PATTERNS,
            ),

            watchlist=cls._find_columns(
                columns,
                WATCHLIST_PATTERNS,
            ),

            adverse_news=cls._find_columns(
                columns,
                ADVERSE_NEWS_PATTERNS,
            ),
        )