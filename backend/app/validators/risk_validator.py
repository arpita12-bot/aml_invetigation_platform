"""
==========================================================
AML Investigation Platform

Risk Validator

Responsibilities
----------------
✓ Validate Risk Score
✓ Validate Risk Level
✓ Validate PEP Status
✓ Validate Sanctions Status
✓ Validate Watchlist Status
✓ Validate Adverse News Status
✓ Check Risk Consistency
✓ Calculate Risk Quality Score

==========================================================
"""

from __future__ import annotations

import pandas as pd

from app.validators.base_validator import (
    BaseValidator,
    ValidationResult,
)
from app.validators.column_detector import DetectedColumns


class RiskValidator(BaseValidator):
    """
    Business validator for AML Risk datasets.
    """

    name = "Risk Validator"

    priority = 140

    supported_columns = []

    VALID_RISK_LEVELS = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY HIGH",
    }

    BOOLEAN_VALUES = {
        "YES",
        "NO",
        "TRUE",
        "FALSE",
        "Y",
        "N",
        "1",
        "0",
    }

    def validate(
        self,
        dataframe: pd.DataFrame,
        detected_columns: DetectedColumns,
    ) -> ValidationResult:

        result = self.create_result()

        # -----------------------------------------
        # Risk Score
        # -----------------------------------------

        missing_scores = 0
        invalid_scores = 0

        risk_scores = None

        if detected_columns.risk_score:

            column = detected_columns.risk_score[0]

            risk_scores = pd.to_numeric(
                dataframe[column],
                errors="coerce",
            )

            missing_scores = risk_scores.isna().sum()

            invalid_scores = (
                (risk_scores < 0)
                | (risk_scores > 100)
            ).sum()

            if missing_scores:

                self.add_warning(
                    result,
                    f"{missing_scores} missing risk scores."
                )

            if invalid_scores:

                self.add_error(
                    result,
                    f"{invalid_scores} invalid risk scores."
                )

        # -----------------------------------------
        # Risk Level
        # -----------------------------------------

        missing_levels = 0
        invalid_levels = 0

        risk_levels = None

        if detected_columns.risk_level:

            column = detected_columns.risk_level[0]

            risk_levels = (
                dataframe[column]
                .fillna("")
                .astype(str)
                .str.upper()
                .str.strip()
            )

            missing_levels = (
                risk_levels == ""
            ).sum()

            invalid_levels = (
                ~risk_levels.isin(
                    self.VALID_RISK_LEVELS
                )
            ).sum()

            if missing_levels:

                self.add_warning(
                    result,
                    f"{missing_levels} missing risk levels."
                )

            if invalid_levels:

                self.add_error(
                    result,
                    f"{invalid_levels} invalid risk levels."
                )

        # -----------------------------------------
        # Boolean AML Flags
        # -----------------------------------------

        def validate_flag(columns, name):

            if not columns:
                return 0, 0

            values = (
                dataframe[columns[0]]
                .fillna("")
                .astype(str)
                .str.upper()
                .str.strip()
            )

            missing = (
                values == ""
            ).sum()

            invalid = (
                ~values.isin(
                    self.BOOLEAN_VALUES
                )
            ).sum()

            if missing:

                self.add_warning(
                    result,
                    f"{missing} missing {name} values."
                )

            if invalid:

                self.add_warning(
                    result,
                    f"{invalid} invalid {name} values."
                )

            return missing, invalid

        pep_missing, pep_invalid = validate_flag(
            detected_columns.pep,
            "PEP",
        )

        sanction_missing, sanction_invalid = validate_flag(
            detected_columns.sanctions,
            "Sanction",
        )

        watchlist_missing, watchlist_invalid = validate_flag(
            detected_columns.watchlist,
            "Watchlist",
        )

        adverse_missing, adverse_invalid = validate_flag(
            detected_columns.adverse_news,
            "Adverse News",
        )

        # -----------------------------------------
        # Risk Consistency
        # -----------------------------------------

        inconsistent = 0

        if (
            risk_scores is not None
            and risk_levels is not None
        ):

            for score, level in zip(
                risk_scores,
                risk_levels,
            ):

                if pd.isna(score):
                    continue

                expected = "LOW"

                if score >= 80:
                    expected = "VERY HIGH"

                elif score >= 60:
                    expected = "HIGH"

                elif score >= 30:
                    expected = "MEDIUM"

                if level != expected:
                    inconsistent += 1

            if inconsistent:

                self.add_warning(
                    result,
                    f"{inconsistent} inconsistent risk classifications."
                )

        # -----------------------------------------
        # Statistics
        # -----------------------------------------

        total_records = len(dataframe)

        quality = (
            (
                total_records
                - missing_scores
                - invalid_scores
            )
            / max(total_records, 1)
        ) * 100

        self.add_statistic(
            result,
            "total_records",
            total_records,
        )

        self.add_statistic(
            result,
            "missing_scores",
            missing_scores,
        )

        self.add_statistic(
            result,
            "invalid_scores",
            invalid_scores,
        )

        self.add_statistic(
            result,
            "missing_levels",
            missing_levels,
        )

        self.add_statistic(
            result,
            "invalid_levels",
            invalid_levels,
        )

        self.add_statistic(
            result,
            "pep_missing",
            pep_missing,
        )

        self.add_statistic(
            result,
            "sanction_missing",
            sanction_missing,
        )

        self.add_statistic(
            result,
            "watchlist_missing",
            watchlist_missing,
        )

        self.add_statistic(
            result,
            "adverse_news_missing",
            adverse_missing,
        )

        self.add_statistic(
            result,
            "risk_inconsistencies",
            inconsistent,
        )

        self.add_statistic(
            result,
            "risk_quality_score",
            round(quality, 2),
        )

        return result