"""
==========================================================
AML Investigation Platform

Hash Utility Functions

Responsibilities
----------------
✓ File SHA-256 hashing
✓ Row-level hashing
✓ DataFrame hashing
✓ Stable entity hashing
✓ Duplicate detection support

==========================================================
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd


# ==========================================================
# File Hash
# ==========================================================

def calculate_file_hash(
    file_path: str | Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate SHA-256 hash of a file.

    Used to detect duplicate uploads.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            chunk = file.read(chunk_size)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================================
# Row Hash
# ==========================================================

def calculate_row_hash(row: pd.Series) -> str:
    """
    Calculate a stable SHA-256 hash for a dataframe row.
    """

    values = []

    for value in row:

        if pd.isna(value):
            values.append("NULL")
        else:
            values.append(str(value).strip())

    row_string = "|".join(values)

    return hashlib.sha256(
        row_string.encode("utf-8")
    ).hexdigest()


# ==========================================================
# DataFrame Row Hashes
# ==========================================================

def add_row_hash_column(
    dataframe: pd.DataFrame,
    column_name: str = "__row_hash__",
) -> pd.DataFrame:
    """
    Add a row hash column.

    Used for incremental loading.
    """

    df = dataframe.copy()

    df[column_name] = df.apply(
        calculate_row_hash,
        axis=1,
    )

    return df


# ==========================================================
# Generic Hash
# ==========================================================

def calculate_hash(value: Any) -> str:
    """
    Generate SHA-256 hash from any value.
    """

    if value is None:
        value = ""

    return hashlib.sha256(
        str(value).encode("utf-8")
    ).hexdigest()


# ==========================================================
# Entity Hash
# ==========================================================

def calculate_entity_hash(
    entity: dict,
    keys: list[str],
) -> str:
    """
    Generate a deterministic hash for an entity.

    Example:
    Customer Name + DOB + Country
    """

    values = []

    for key in keys:

        value = entity.get(key)

        if value is None:
            value = ""

        values.append(
            str(value).strip().lower()
        )

    entity_string = "|".join(values)

    return hashlib.sha256(
        entity_string.encode("utf-8")
    ).hexdigest()


# ==========================================================
# DataFrame Hash
# ==========================================================

def calculate_dataframe_hash(
    dataframe: pd.DataFrame,
) -> str:
    """
    Generate a stable hash for a dataframe.
    """

    csv_string = dataframe.to_csv(
        index=False
    )

    return hashlib.sha256(
        csv_string.encode("utf-8")
    ).hexdigest()