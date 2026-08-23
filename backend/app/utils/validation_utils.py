"""
==========================================================
AML Investigation Platform

Validation Utility Functions

Responsibilities
----------------
✓ Email Validation
✓ Phone Validation
✓ Date Validation
✓ Numeric Validation
✓ Null Percentage
✓ Duplicate Percentage
✓ DataFrame Validation
✓ Schema Validation

==========================================================
"""

from __future__ import annotations

import re
from datetime import datetime

import pandas as pd

from app.core.exceptions import (
    DatasetValidationError,
    SchemaValidationError,
)

# ==========================================================
# Regular Expressions
# ==========================================================

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_REGEX = re.compile(
    r"^\+?[0-9]{7,15}$"
)

CURRENCY_REGEX = re.compile(
    r"^[A-Z]{3}$"
)

COUNTRY_REGEX = re.compile(
    r"^[A-Z]{2}$"
)

# ==========================================================
# Email Validation
# ==========================================================

def is_valid_email(email: str) -> bool:

    if pd.isna(email):
        return False

    return bool(
        EMAIL_REGEX.match(
            str(email).strip()
        )
    )
    
# ==========================================================
# Phone Validation
# ==========================================================

def is_valid_phone(phone: str) -> bool:

    if pd.isna(phone):
        return False

    phone = (
        str(phone)
        .replace(" ", "")
        .replace("-", "")
    )

    return bool(
        PHONE_REGEX.match(phone)
    )
    
# ==========================================================
# Date Validation
# ==========================================================

def is_valid_date(value) -> bool:

    try:

        pd.to_datetime(value)

        return True

    except Exception:

        return False
    
# ==========================================================
# Numeric Validation
# ==========================================================

def is_numeric(value) -> bool:

    try:

        float(value)

        return True

    except Exception:

        return False
    
# ==========================================================
# Currency Validation
# ==========================================================

def is_valid_currency(currency: str) -> bool:

    if pd.isna(currency):
        return False

    return bool(
        CURRENCY_REGEX.match(
            str(currency).upper()
        )
    )
    
# ==========================================================
# Country Validation
# ==========================================================

def is_valid_country(country: str) -> bool:

    if pd.isna(country):
        return False

    return bool(
        COUNTRY_REGEX.match(
            str(country).upper()
        )
    )
    
# ==========================================================
# Empty DataFrame
# ==========================================================

def validate_dataframe(
    dataframe: pd.DataFrame,
) -> None:

    if dataframe.empty:

        raise DatasetValidationError(
            "Dataset is empty."
        )
        
# ==========================================================
# Duplicate Columns
# ==========================================================

def validate_columns(
    dataframe: pd.DataFrame,
) -> None:

    duplicated = dataframe.columns.duplicated()

    if duplicated.any():

        raise SchemaValidationError(
            "Duplicate column names detected."
        )
        
# ==========================================================
# Missing Percentage
# ==========================================================

def missing_percentage(
    dataframe: pd.DataFrame,
) -> float:

    total = (
        dataframe.isna()
        .sum()
        .sum()
    )

    cells = (
        len(dataframe)
        * len(dataframe.columns)
    )

    if cells == 0:
        return 0.0

    return round(
        (total / cells) * 100,
        2,
    )
    
# ==========================================================
# Duplicate Percentage
# ==========================================================

def duplicate_percentage(
    dataframe: pd.DataFrame,
) -> float:

    if dataframe.empty:
        return 0.0

    duplicates = dataframe.duplicated().sum()

    return round(
        (duplicates / len(dataframe)) * 100,
        2,
    )
    
# ==========================================================
# Validation Summary
# ==========================================================

def validation_summary(
    dataframe: pd.DataFrame,
) -> dict:

    return {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "missing_percentage":
            missing_percentage(dataframe),

        "duplicate_percentage":
            duplicate_percentage(dataframe),
    }