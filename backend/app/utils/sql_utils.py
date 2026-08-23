"""
==========================================================
AML Investigation Platform

SQL Utility Functions

Responsibilities
----------------
✓ Generate SQL-safe table names
✓ Generate SQL-safe column names
✓ Validate PostgreSQL identifiers
✓ Handle reserved keywords
✓ Infer SQLAlchemy column types
✓ Generate CREATE TABLE statements
✓ Prevent SQL Injection

==========================================================
"""

import keyword
import re
from typing import Dict
from app.core.constants import POSTGRES_RESERVED_WORDS


import pandas as pd
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Numeric,
    String,
    Text,
)

from app.core.config import settings


# ==========================================================
# Identifier Sanitization
# ==========================================================

def sanitize_identifier(name: str) -> str:
    """
    Convert any string into a PostgreSQL-safe identifier.
    """

    if not name:
        raise ValueError("Identifier cannot be empty.")

    name = name.strip().lower()

    # Replace spaces and separators
    name = re.sub(r"[ \-./\\]+", "_", name)

    # Remove invalid characters
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)

    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    # Cannot begin with number
    if name and name[0].isdigit():
        name = f"t_{name}"

    # Python keyword
    if keyword.iskeyword(name):
        name += "_col"

    # PostgreSQL keyword
    if name in POSTGRES_RESERVED_WORDS:
        name += "_col"

    # Maximum identifier length
    return name[: settings.MAX_TABLE_NAME_LENGTH]


# ==========================================================
# Table Name
# ==========================================================

def generate_table_name(filename: str) -> str:
    """
    Generate PostgreSQL table name from filename.
    """

    filename = filename.rsplit(".", 1)[0]

    return sanitize_identifier(filename)


# ==========================================================
# Column Name
# ==========================================================

def generate_column_name(column: str) -> str:
    """
    Generate PostgreSQL-safe column name.
    """

    return sanitize_identifier(column)[: settings.MAX_COLUMN_NAME_LENGTH]


# ==========================================================
# Duplicate Column Handling
# ==========================================================

def normalize_column_names(columns: list[str]) -> list[str]:
    """
    Ensure column names are unique.
    """

    seen = {}

    normalized = []

    for col in columns:

        col = generate_column_name(col)

        if col not in seen:
            seen[col] = 1
            normalized.append(col)
        else:
            seen[col] += 1
            normalized.append(f"{col}_{seen[col]}")

    return normalized


# ==========================================================
# SQLAlchemy Type Inference
# ==========================================================

def infer_sqlalchemy_type(series: pd.Series):
    """
    Infer SQLAlchemy datatype from Pandas Series.
    """

    dtype = series.dtype

    if pd.api.types.is_integer_dtype(dtype):
        return Integer

    if pd.api.types.is_float_dtype(dtype):
        return Float

    if pd.api.types.is_bool_dtype(dtype):
        return Boolean

    if pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime

    if pd.api.types.is_object_dtype(dtype):

        max_length = (
            series.astype(str)
            .map(len)
            .max()
        )

        if pd.isna(max_length):
            return Text

        if max_length <= 255:
            return String(255)

        return Text

    return Text


# ==========================================================
# Detect Decimal Columns
# ==========================================================

def infer_numeric_precision(series: pd.Series):
    """
    Return Numeric for high precision decimal values.
    """

    if not pd.api.types.is_numeric_dtype(series):
        return None

    sample = series.dropna().astype(str).head(100)

    decimal_places = 0

    for value in sample:

        if "." in value:

            places = len(value.split(".")[1])

            decimal_places = max(decimal_places, places)

    if decimal_places > 6:
        return Numeric(38, 10)

    return None


# ==========================================================
# Schema Mapping
# ==========================================================

def dataframe_schema(df: pd.DataFrame) -> Dict[str, object]:
    """
    Convert dataframe into SQLAlchemy schema mapping.
    """

    schema = {}

    for column in df.columns:

        numeric = infer_numeric_precision(df[column])

        if numeric is not None:
            schema[column] = numeric
        else:
            schema[column] = infer_sqlalchemy_type(df[column])

    return schema


# ==========================================================
# Identifier Validation
# ==========================================================

def is_valid_identifier(name: str) -> bool:
    """
    Validate PostgreSQL identifier.
    """

    pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"

    return bool(re.match(pattern, name))