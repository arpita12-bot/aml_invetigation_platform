"""
==========================================================
AML Investigation Platform

Semantic Detector

Responsibilities
----------------
✓ Infer business meaning of columns
✓ Populate SemanticMetadata
✓ Confidence-based matching
✓ Alias matching

==========================================================
"""

from __future__ import annotations

from app.core.column_patterns import SEMANTIC_PATTERNS
from app.models.schema.column_metadata import ColumnMetadata
from app.models.schema.semantic_metadata import SemanticMetadata


class SemanticDetector:
    """
    Detect semantic meaning of dataset columns.
    """

    @classmethod
    def detect(
        cls,
        columns: list[ColumnMetadata],
    ) -> list[ColumnMetadata]:

        for column in columns:

            column.semantic = cls.detect_column(
                column.name
            )

        return columns

    @classmethod
    def detect_column(
        cls,
        column_name: str,
    ) -> SemanticMetadata:

        normalized = (
            column_name
            .lower()
            .replace(" ", "_")
        )

        # ----------------------------------------
        # Exact Match
        # ----------------------------------------

        for semantic_type, aliases in SEMANTIC_PATTERNS.items():

            if normalized in aliases:

                return SemanticMetadata(

                    semantic_type=semantic_type,

                    confidence=100.0,

                    matched_alias=normalized,

                    detection_method="EXACT_PATTERN",

                    evidence=[
                        f"Exact alias match '{normalized}'."
                    ]

                )

        # ----------------------------------------
        # Partial Match
        # ----------------------------------------

        for semantic_type, aliases in SEMANTIC_PATTERNS.items():

            for alias in aliases:

                if alias in normalized:

                    return SemanticMetadata(

                        semantic_type=semantic_type,

                        confidence=85.0,

                        matched_alias=alias,

                        detection_method="PARTIAL_PATTERN",

                        evidence=[
                            f"Partial alias match '{alias}'."
                        ]

                    )

        # ----------------------------------------
        # Unknown
        # ----------------------------------------

        return SemanticMetadata(

            semantic_type="UNKNOWN",

            confidence=0.0,

            matched_alias=None,

            detection_method="NONE",

            evidence=[
                "No semantic pattern matched."
            ]

        )