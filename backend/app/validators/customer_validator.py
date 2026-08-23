"""
==========================================================
AML Investigation Platform

Customer Validator

Responsibilities
----------------
✓ Validate customer identifiers
✓ Validate customer names
✓ Detect duplicate customer IDs
✓ Detect missing mandatory fields
✓ Calculate customer data quality metrics

==========================================================
"""

from __future__ import annotations

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class CustomerValidator(BaseValidator):
    """
    Business validator for customer datasets.
    """

    name = "Customer Validator"

    priority = 100

    supported_columns = []

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        # --------------------------------------------------
        # Customer ID
        # --------------------------------------------------

        customer_columns = detected_columns.customer

        if not customer_columns:

            self.add_warning(
                result,
                "Customer ID column not found."
            )

            return result

        customer_column = customer_columns[0]

        customer_ids = (
            dataframe[customer_column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Missing IDs
        # --------------------------------------------------

        missing_customer_ids = (
            customer_ids == ""
        ).sum()

        if missing_customer_ids:

            self.add_error(
                result,
                f"{missing_customer_ids} customer IDs are missing."
            )

        # --------------------------------------------------
        # Duplicate IDs
        # --------------------------------------------------

        duplicate_customer_ids = (
            customer_ids.duplicated().sum()
        )

        if duplicate_customer_ids:

            self.add_error(
                result,
                f"{duplicate_customer_ids} duplicate customer IDs found."
            )

        # --------------------------------------------------
        # Customer Name
        # --------------------------------------------------

        if detected_columns.customer_name:

            name_column = detected_columns.customer_name[0]

            names = (
                dataframe[name_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

        else:

            first = (
                detected_columns.first_name[0]
                if detected_columns.first_name
                else None
            )

            last = (
                detected_columns.last_name[0]
                if detected_columns.last_name
                else None
            )

            if first and last:

                names = (
                    dataframe[first]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    + " "
                    + dataframe[last]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

            else:

                names = None

        # --------------------------------------------------
        # Missing Names
        # --------------------------------------------------

        missing_names = 0

        if names is not None:

            missing_names = (
                names.str.strip() == ""
            ).sum()

            if missing_names:

                self.add_warning(
                    result,
                    f"{missing_names} customer names are missing."
                )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        total_customers = len(customer_ids)

        unique_customers = customer_ids.nunique()

        quality_score = (
            (
                total_customers
                - missing_customer_ids
                - duplicate_customer_ids
            )
            / max(total_customers, 1)
        ) * 100

        self.add_statistic(
            result,
            "total_customers",
            total_customers,
        )

        self.add_statistic(
            result,
            "unique_customers",
            unique_customers,
        )

        self.add_statistic(
            result,
            "missing_customer_ids",
            missing_customer_ids,
        )

        self.add_statistic(
            result,
            "duplicate_customer_ids",
            duplicate_customer_ids,
        )

        self.add_statistic(
            result,
            "missing_customer_names",
            missing_names,
        )

        self.add_statistic(
            result,
            "customer_quality_score",
            round(quality_score, 2),
        )

        return result