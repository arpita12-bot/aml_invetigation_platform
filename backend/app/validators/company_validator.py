"""
==========================================================
AML Investigation Platform

Company Validator

Responsibilities
----------------
✓ Validate company identifiers
✓ Validate company names
✓ Validate tax identifiers
✓ Detect duplicate companies
✓ Detect missing mandatory fields
✓ Calculate company data quality metrics

==========================================================
"""

from __future__ import annotations

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class CompanyValidator(BaseValidator):
    """
    Business validator for company datasets.
    """

    name = "Company Validator"

    priority = 120

    supported_columns = []

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        # --------------------------------------------------
        # Company ID
        # --------------------------------------------------

        company_columns = detected_columns.company

        if not company_columns:

            self.add_warning(
                result,
                "Company ID/Company Name column not found."
            )

            return result

        company_column = company_columns[0]

        companies = (
            dataframe[company_column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # --------------------------------------------------
        # Missing Companies
        # --------------------------------------------------

        missing_companies = (
            companies == ""
        ).sum()

        if missing_companies:

            self.add_error(
                result,
                f"{missing_companies} companies are missing."
            )

        # --------------------------------------------------
        # Duplicate Companies
        # --------------------------------------------------

        duplicate_companies = (
            companies.duplicated().sum()
        )

        if duplicate_companies:

            self.add_warning(
                result,
                f"{duplicate_companies} duplicate companies found."
            )

        # --------------------------------------------------
        # Tax ID
        # --------------------------------------------------

        missing_tax_ids = 0

        duplicate_tax_ids = 0

        if detected_columns.tax_id:

            tax_column = detected_columns.tax_id[0]

            tax_ids = (
                dataframe[tax_column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            missing_tax_ids = (
                tax_ids == ""
            ).sum()

            duplicate_tax_ids = (
                tax_ids.duplicated().sum()
            )

            if missing_tax_ids:

                self.add_warning(
                    result,
                    f"{missing_tax_ids} tax identifiers are missing."
                )

            if duplicate_tax_ids:

                self.add_warning(
                    result,
                    f"{duplicate_tax_ids} duplicate tax identifiers found."
                )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        total_companies = len(companies)

        unique_companies = companies.nunique()

        quality_score = (
            (
                total_companies
                - missing_companies
                - duplicate_companies
            )
            / max(total_companies, 1)
        ) * 100

        self.add_statistic(
            result,
            "total_companies",
            total_companies,
        )

        self.add_statistic(
            result,
            "unique_companies",
            unique_companies,
        )

        self.add_statistic(
            result,
            "missing_companies",
            missing_companies,
        )

        self.add_statistic(
            result,
            "duplicate_companies",
            duplicate_companies,
        )

        self.add_statistic(
            result,
            "missing_tax_ids",
            missing_tax_ids,
        )

        self.add_statistic(
            result,
            "duplicate_tax_ids",
            duplicate_tax_ids,
        )

        self.add_statistic(
            result,
            "company_quality_score",
            round(quality_score, 2),
        )

        return result