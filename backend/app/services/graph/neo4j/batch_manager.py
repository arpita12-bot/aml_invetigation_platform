"""
Batch Manager
"""

from __future__ import annotations


class BatchManager:

    @staticmethod
    def batches(
        items,
        batch_size: int = 5000,
    ):

        for index in range(

            0,

            len(items),

            batch_size,

        ):

            yield items[
                index:index + batch_size
            ]