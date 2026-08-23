"""
==========================================================
AML Investigation Platform

Batch Generator

Responsibilities
----------------
✓ Split DataFrames into batches

==========================================================
"""

from __future__ import annotations

import pandas as pd


class BatchGenerator:
    """
    Splits a DataFrame into batches.
    """

    @staticmethod
    def generate(
        dataframe: pd.DataFrame,
        batch_size: int = 5000,
    ):

        total = len(dataframe)

        for start in range(
            0,
            total,
            batch_size,
        ):

            yield dataframe.iloc[
                start:start + batch_size
            ]