"""
==========================================================
AML Investigation Platform

DataFrame Utility Functions

Responsibilities
----------------
✓ Read CSV / Excel / JSON
✓ Normalize column names
✓ Remove empty rows & columns
✓ Standardize missing values
✓ Optimize memory
✓ Optimize datatypes
✓ DataFrame statistics

==========================================================
"""

from pathlib import Path

import pandas as pd

from app.core.exceptions import UnsupportedFileTypeError
from app.utils.sql_utils import normalize_column_names

# ==========================================================
# Read Dataset
# ==========================================================

def read_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Read supported dataset formats with encoding fallback.
    """

    path = Path(file_path)

    suffix = path.suffix.lower()

    try:

        if suffix == ".csv":

            try:
                return pd.read_csv(path, encoding="utf-8")

            except UnicodeDecodeError:
                return pd.read_csv(path, encoding="latin-1")

        if suffix in [".xlsx", ".xls"]:
            return pd.read_excel(path)

        if suffix == ".json":
            return pd.read_json(path)

        raise UnsupportedFileTypeError(
            f"Unsupported file format: {suffix}"
        )

    except Exception as e:
        raise UnsupportedFileTypeError(str(e)) from e

# ==========================================================
# Normalize Columns
# ==========================================================

def normalize_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normalize dataframe column names.
    """

    df = dataframe.copy()

    df.columns = normalize_column_names(
        list(df.columns)
    )

    return df


# ==========================================================
# Remove Empty Rows
# ==========================================================

def remove_empty_rows(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    return dataframe.dropna(
        how="all"
    ).reset_index(drop=True)


# ==========================================================
# Remove Empty Columns
# ==========================================================

def remove_empty_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    return dataframe.dropna(
        axis=1,
        how="all"
    )


# ==========================================================
# Trim Strings
# ==========================================================

def trim_whitespace(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    df = dataframe.copy()

    object_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in object_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    return df


# ==========================================================
# Standardize Missing Values
# ==========================================================

def standardize_missing_values(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    df = dataframe.copy()

    replacements = {
        "": pd.NA,
        " ": pd.NA,
        "NULL": pd.NA,
        "null": pd.NA,
        "N/A": pd.NA,
        "n/a": pd.NA,
        "NA": pd.NA,
        "-": pd.NA,
    }

    return df.replace(replacements)
# ==========================================================
# Memory Usage
# ==========================================================

def dataframe_memory_usage(
    dataframe: pd.DataFrame,
) -> float:

    return (
        dataframe.memory_usage(deep=True)
        .sum()
        / 1024
        / 1024
    )


# ==========================================================
# DataFrame Statistics
# ==========================================================

def dataframe_statistics(
    dataframe: pd.DataFrame,
) -> dict:

    return {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "memory_mb": round(
            dataframe_memory_usage(dataframe),
            2,
        ),

        "duplicate_rows":
            dataframe.duplicated().sum(),

        "total_missing":

            dataframe.isna().sum().sum(),
    }
    
# ==========================================================
# Clean DataFrame Pipeline
# ==========================================================

def clean_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standard preprocessing pipeline.
    """

    df = normalize_columns(dataframe)

    df = remove_empty_rows(df)

    df = remove_empty_columns(df)

    df = remove_duplicate_rows(df)

    df = trim_whitespace(df)

    df = standardize_missing_values(df)

    df = optimize_dataframe(df)

    return df
# ==========================================================
# Remove Duplicate Rows
# ==========================================================

def remove_duplicate_rows(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    return dataframe.drop_duplicates().reset_index(drop=True)

def optimize_integer_columns(df: pd.DataFrame) -> pd.DataFrame:

    dataframe = df.copy()

    columns = dataframe.select_dtypes(include=["int64"]).columns

    for column in columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            downcast="integer"
        )

    return dataframe

def optimize_float_columns(df: pd.DataFrame) -> pd.DataFrame:

    dataframe = df.copy()

    columns = dataframe.select_dtypes(include=["float64"]).columns

    for column in columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            downcast="float"
        )

    return dataframe

def optimize_object_columns(
    df: pd.DataFrame,
    threshold: float = 0.5,
) -> pd.DataFrame:

    dataframe = df.copy()

    columns = dataframe.select_dtypes(include=["object"]).columns

    for column in columns:

        ratio = dataframe[column].nunique(dropna=True) / max(len(dataframe), 1)

        if ratio < threshold:
            dataframe[column] = dataframe[column].astype("category")

    return dataframe

def optimize_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Optimize dataframe memory usage.
    """

    df = optimize_integer_columns(dataframe)

    df = optimize_float_columns(df)

    df = optimize_object_columns(df)

    return df