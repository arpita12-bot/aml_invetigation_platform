"""
==========================================================
AML Investigation Platform

Dataset Loader

Responsibilities
----------------
✓ Load CSV
✓ Load Excel
✓ Load Parquet
✓ Load JSON
✓ Normalize columns
✓ Infer metadata

==========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


class DatasetLoader:
    """
    Enterprise Dataset Loader.
    """

    SUPPORTED_TYPES = {
        ".csv",
        ".xlsx",
        ".xls",
        ".json",
        ".parquet",
    }

    # -----------------------------------------------------

    def load(self, file_path: str) -> pd.DataFrame:

        file_path = Path(file_path)

        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".csv":
            df = pd.read_csv(file_path)

        elif extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)

        elif extension == ".json":
            df = pd.read_json(file_path)

        elif extension == ".parquet":
            df = pd.read_parquet(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return self.normalize_columns(df)

    # -----------------------------------------------------

    def normalize_columns(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
            .str.replace("/", "_")
        )

        return df

    # -----------------------------------------------------

    def infer_metadata(
        self,
        df: pd.DataFrame,
    ) -> Dict:

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "column_names": list(df.columns),

            "data_types": {
                c: str(df[c].dtype)
                for c in df.columns
            },

            "memory_mb": round(

                df.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024,

                2,
            ),
        }

    # -----------------------------------------------------

    def detect_dataset_name(
        self,
        file_path: str,
    ) -> str:

        return Path(file_path).stem.lower()

    # -----------------------------------------------------

    def preview(
        self,
        df: pd.DataFrame,
        rows: int = 10,
    ):

        return df.head(rows)