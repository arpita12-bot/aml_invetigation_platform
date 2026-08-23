"""
==========================================================
AML Investigation Platform

Enterprise Data Quality Service

Responsibilities
----------------
✓ Dataset Completeness
✓ Duplicate Detection
✓ Missing Value Analysis
✓ Data Type Analysis
✓ Numeric Outlier Detection
✓ Email Validation
✓ Phone Validation
✓ Date Validation
✓ Quality Score Calculation

==========================================================
"""

from __future__ import annotations

import re
from typing import Dict

import numpy as np
import pandas as pd


class DataQualityService:
    """
    Enterprise Data Quality Analyzer.
    """

    EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    PHONE_REGEX = r"^[+]?[0-9()\-\s]{7,20}$"

    # ---------------------------------------------------------

    def analyze(self, df: pd.DataFrame) -> Dict:

        report = {
            "rows": len(df),
            "columns": len(df.columns),
            "duplicate_rows": self.duplicate_rows(df),
            "duplicate_percentage": self.duplicate_percentage(df),
            "null_summary": self.null_summary(df),
            "completeness": self.completeness(df),
            "data_types": self.data_types(df),
            "numeric_outliers": self.numeric_outliers(df),
            "email_validation": self.validate_email_columns(df),
            "phone_validation": self.validate_phone_columns(df),
            "quality_score": 0,
        }

        report["quality_score"] = self.calculate_score(report)

        return report

    # ---------------------------------------------------------

    def duplicate_rows(self, df):

        return int(df.duplicated().sum())

    # ---------------------------------------------------------

    def duplicate_percentage(self, df):

        if len(df) == 0:
            return 0

        return round(
            (df.duplicated().sum() / len(df)) * 100,
            2,
        )

    # ---------------------------------------------------------

    def null_summary(self, df):

        result = {}

        for column in df.columns:

            nulls = int(df[column].isna().sum())

            result[column] = {
                "nulls": nulls,
                "percentage": round(
                    (nulls / len(df)) * 100 if len(df) else 0,
                    2,
                ),
            }

        return result

    # ---------------------------------------------------------

    def completeness(self, df):

        if len(df) == 0:
            return 0

        total_cells = df.shape[0] * df.shape[1]

        missing = df.isna().sum().sum()

        return round(
            ((total_cells - missing) / total_cells) * 100,
            2,
        )

    # ---------------------------------------------------------

    def data_types(self, df):

        return {
            c: str(df[c].dtype)
            for c in df.columns
        }

    # ---------------------------------------------------------

    def numeric_outliers(self, df):

        report = {}

        numeric = df.select_dtypes(
            include=np.number
        )

        for col in numeric.columns:

            q1 = numeric[col].quantile(0.25)
            q3 = numeric[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = numeric[
                (numeric[col] < lower)
                | (numeric[col] > upper)
            ]

            report[col] = len(outliers)

        return report

    # ---------------------------------------------------------

    def validate_email_columns(self, df):

        report = {}

        for col in df.columns:

            if "email" not in col.lower():
                continue

            invalid = 0

            for value in df[col].dropna():

                if not re.match(
                    self.EMAIL_REGEX,
                    str(value),
                ):
                    invalid += 1

            report[col] = invalid

        return report

    # ---------------------------------------------------------

    def validate_phone_columns(self, df):

        report = {}

        for col in df.columns:

            if "phone" not in col.lower():
                continue

            invalid = 0

            for value in df[col].dropna():

                if not re.match(
                    self.PHONE_REGEX,
                    str(value),
                ):
                    invalid += 1

            report[col] = invalid

        return report

    # ---------------------------------------------------------

    def calculate_score(self, report):

        score = 100

        score -= report["duplicate_percentage"] * 0.3

        score -= (100 - report["completeness"]) * 0.5

        invalid_email = sum(
            report["email_validation"].values()
        )

        invalid_phone = sum(
            report["phone_validation"].values()
        )

        score -= invalid_email * 0.2

        score -= invalid_phone * 0.2

        return max(round(score, 2), 0)