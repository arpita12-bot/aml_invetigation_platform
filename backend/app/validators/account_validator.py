"""
==========================================================
AML Investigation Platform

Account Validator

Responsibilities
----------------
✓ Validate account identifiers
✓ Validate account types
✓ Validate bank names
✓ Detect duplicate account IDs
✓ Detect missing mandatory fields
✓ Calculate account data quality metrics

==========================================================
"""

from __future__ import annotations

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class AccountValidator(BaseValidator):
    """
    Business validator for account datasets.
    """

    name = "Account Validator"

    priority = 110

    supported_columns = []

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        # --------------------------------------------------
        # Account ID
        # --------------------------------------------------

        account_columns = detected_columns.account

        if not account_columns:

            self.add_warning(
                result,
                "Account ID column not found."
            )

            return result

        account_column = account_columns[0]

        account_ids = (
            dataframe[account_column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Missing Account IDs
        # --------------------------------------------------

        missing_account_ids = (
            account_ids == ""
        ).sum()

        if missing_account_ids:

            self.add_error(
                result,
                f"{missing_account_ids} account IDs are missing."
            )

        # --------------------------------------------------
        # Duplicate Account IDs
        # --------------------------------------------------

        duplicate_account_ids = (
            account_ids.duplicated().sum()
        )

        if duplicate_account_ids:

            self.add_error(
                result,
                f"{duplicate_account_ids} duplicate account IDs found."
            )

        # --------------------------------------------------
        # Account Type
        # --------------------------------------------------

        missing_account_types = 0

        if detected_columns.account_type:

            account_type_column = detected_columns.account_type[0]

            account_types = (
                dataframe[account_type_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            missing_account_types = (
                account_types == ""
            ).sum()

            if missing_account_types:

                self.add_warning(
                    result,
                    f"{missing_account_types} account types are missing."
                )

        # --------------------------------------------------
        # Bank Name
        # --------------------------------------------------

        missing_bank_names = 0

        if detected_columns.bank:

            bank_column = detected_columns.bank[0]

            banks = (
                dataframe[bank_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            missing_bank_names = (
                banks == ""
            ).sum()

            if missing_bank_names:

                self.add_warning(
                    result,
                    f"{missing_bank_names} bank names are missing."
                )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        total_accounts = len(account_ids)

        unique_accounts = account_ids.nunique()

        quality_score = (
            (
                total_accounts
                - missing_account_ids
                - duplicate_account_ids
            )
            / max(total_accounts, 1)
        ) * 100

        self.add_statistic(
            result,
            "total_accounts",
            total_accounts,
        )

        self.add_statistic(
            result,
            "unique_accounts",
            unique_accounts,
        )

        self.add_statistic(
            result,
            "missing_account_ids",
            missing_account_ids,
        )

        self.add_statistic(
            result,
            "duplicate_account_ids",
            duplicate_account_ids,
        )

        self.add_statistic(
            result,
            "missing_account_types",
            missing_account_types,
        )

        self.add_statistic(
            result,
            "missing_bank_names",
            missing_bank_names,
        )

        self.add_statistic(
            result,
            "account_quality_score",
            round(quality_score, 2),
        )

        return result