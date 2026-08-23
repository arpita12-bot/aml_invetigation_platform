"""
==========================================================
AML Investigation Platform

Transaction Validator

Responsibilities
----------------
✓ Validate transaction identifiers
✓ Validate transaction amounts
✓ Validate currencies
✓ Validate transaction dates
✓ Detect duplicate transactions
✓ Detect missing mandatory fields
✓ Detect suspicious transaction values
✓ Calculate transaction quality metrics

==========================================================
"""

from __future__ import annotations

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class TransactionValidator(BaseValidator):
    """
    Business validator for transaction datasets.
    """

    name = "Transaction Validator"

    priority = 130

    supported_columns = []

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        # --------------------------------------------------
        # Transaction ID
        # --------------------------------------------------

        transaction_columns = detected_columns.transaction

        if not transaction_columns:

            self.add_warning(
                result,
                "Transaction ID column not found."
            )

            return result

        transaction_column = transaction_columns[0]

        transaction_ids = (
            dataframe[transaction_column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Missing Transaction IDs
        # --------------------------------------------------

        missing_transaction_ids = (
            transaction_ids == ""
        ).sum()

        if missing_transaction_ids:

            self.add_error(
                result,
                f"{missing_transaction_ids} transaction IDs are missing."
            )

        # --------------------------------------------------
        # Duplicate Transaction IDs
        # --------------------------------------------------

        duplicate_transaction_ids = (
            transaction_ids.duplicated().sum()
        )

        if duplicate_transaction_ids:

            self.add_error(
                result,
                f"{duplicate_transaction_ids} duplicate transaction IDs found."
            )

        # --------------------------------------------------
        # Transaction Amount
        # --------------------------------------------------

        invalid_amounts = 0

        negative_amounts = 0

        if detected_columns.amount:

            amount_column = detected_columns.amount[0]

            amounts = pd.to_numeric(
                dataframe[amount_column],
                errors="coerce",
            )

            invalid_amounts = amounts.isna().sum()

            negative_amounts = (amounts <= 0).sum()

            if invalid_amounts:

                self.add_warning(
                    result,
                    f"{invalid_amounts} invalid transaction amounts found."
                )

            if negative_amounts:

                self.add_warning(
                    result,
                    f"{negative_amounts} transactions have zero or negative amounts."
                )

        # --------------------------------------------------
        # Missing Currency
        # --------------------------------------------------

        missing_currency = 0

        if detected_columns.currency:

            currency_column = detected_columns.currency[0]

            currencies = (
                dataframe[currency_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            missing_currency = (
                currencies == ""
            ).sum()

            if missing_currency:

                self.add_warning(
                    result,
                    f"{missing_currency} transactions have missing currency."
                )

        # --------------------------------------------------
        # Missing Transaction Date
        # --------------------------------------------------

        missing_dates = 0

        if detected_columns.date:

            date_column = detected_columns.date[0]

            dates = (
                dataframe[date_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            missing_dates = (
                dates == ""
            ).sum()

            if missing_dates:

                self.add_warning(
                    result,
                    f"{missing_dates} transactions have missing dates."
                )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        total_transactions = len(transaction_ids)

        unique_transactions = transaction_ids.nunique()

        quality_score = (
            (
                total_transactions
                - missing_transaction_ids
                - duplicate_transaction_ids
            )
            / max(total_transactions, 1)
        ) * 100

        self.add_statistic(
            result,
            "total_transactions",
            total_transactions,
        )

        self.add_statistic(
            result,
            "unique_transactions",
            unique_transactions,
        )

        self.add_statistic(
            result,
            "missing_transaction_ids",
            missing_transaction_ids,
        )

        self.add_statistic(
            result,
            "duplicate_transaction_ids",
            duplicate_transaction_ids,
        )

        self.add_statistic(
            result,
            "invalid_amounts",
            invalid_amounts,
        )

        self.add_statistic(
            result,
            "negative_amounts",
            negative_amounts,
        )

        self.add_statistic(
            result,
            "missing_currency",
            missing_currency,
        )

        self.add_statistic(
            result,
            "missing_dates",
            missing_dates,
        )

        self.add_statistic(
            result,
            "transaction_quality_score",
            round(quality_score, 2),
        )

        return result