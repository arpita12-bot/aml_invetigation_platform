"""
==========================================================
AML Investigation Platform

Key Detector

Responsibilities
----------------
✓ Detect Primary Keys
✓ Detect Foreign Keys
✓ Detect Candidate Keys
✓ Confidence Scoring
✓ Produce KeyMetadata

==========================================================
"""

from __future__ import annotations

import re

import pandas as pd

from app.models.schema.column_metadata import ColumnMetadata
from app.models.schema.key_metadata import KeyMetadata


class KeyDetector:
    """
    Detect keys using rule-based confidence scoring.
    """

    PRIMARY_THRESHOLD = 80
    CANDIDATE_THRESHOLD = 60
    FOREIGN_THRESHOLD = 55

    ID_PATTERN = re.compile(
        r"(id|_id|number|no|code|key)$",
        re.IGNORECASE,
    )

    ENTITY_PATTERN = re.compile(
        r"(customer|account|transaction|company|entity|person|party|client)",
        re.IGNORECASE,
    )

    @classmethod
    def detect(
        cls,
        dataframe: pd.DataFrame,
        columns: list[ColumnMetadata],
    ) -> list[KeyMetadata]:

        detected_keys: list[KeyMetadata] = []

        primary_candidates: list[KeyMetadata] = []

        for column in columns:

            key = cls._score_column(
                dataframe,
                column,
            )

            if key is None:
                continue

            if key.key_type == "PRIMARY":
                primary_candidates.append(key)
            else:
                detected_keys.append(key)

        # Keep only the highest-confidence primary key
        if primary_candidates:

            primary_candidates.sort(
                key=lambda k: k.confidence,
                reverse=True,
            )

            detected_keys.append(primary_candidates[0])

        return detected_keys

    @classmethod
    def _score_column(
        cls,
        dataframe: pd.DataFrame,
        column: ColumnMetadata,
    ) -> KeyMetadata | None:

        score = 0
        reasons = []

        series = dataframe[column.name]

        # --------------------------------------
        # Unique
        # --------------------------------------

        if series.is_unique:

            score += 40

            reasons.append(
                "Column values are unique."
            )

        # --------------------------------------
        # No Nulls
        # --------------------------------------

        if not series.isna().any():

            score += 20

            reasons.append(
                "Column has no null values."
            )

        # --------------------------------------
        # Column Name
        # --------------------------------------

        if cls.ID_PATTERN.search(column.name):

            score += 15

            reasons.append(
                "Column name indicates identifier."
            )

        # --------------------------------------
        # Semantic Type
        # --------------------------------------

        if cls.ENTITY_PATTERN.search(column.name):

            score += 10

            reasons.append(
                "Column name represents business entity."
            )

        # --------------------------------------
        # SQL Type
        # --------------------------------------

        if column.sql_type.startswith(
            (
                "BIGINT",
                "INTEGER",
                "VARCHAR",
            )
        ):

            score += 5

            reasons.append(
                "Suitable SQL datatype."
            )

        # --------------------------------------
        # Cardinality
        # --------------------------------------

        ratio = (
            column.distinct_count
            / max(len(dataframe), 1)
        )

        if ratio >= 0.95:

            score += 10

            reasons.append(
                "High cardinality."
            )

        # --------------------------------------
        # Decide Type
        # --------------------------------------

        if score >= cls.PRIMARY_THRESHOLD:

            return KeyMetadata(

                column_name=column.name,

                key_type="PRIMARY",

                confidence=score,

                reasons=reasons,

            )

        if score >= cls.CANDIDATE_THRESHOLD:

            return KeyMetadata(

                column_name=column.name,

                key_type="CANDIDATE",

                confidence=score,

                reasons=reasons,

            )

        if (
            cls.ID_PATTERN.search(column.name)
            and not series.is_unique
        ):

            return KeyMetadata(

                column_name=column.name,

                key_type="FOREIGN",

                confidence=max(
                    score,
                    cls.FOREIGN_THRESHOLD,
                ),

                reasons=reasons
                + [
                    "Identifier appears multiple times."
                ],

            )

        return None