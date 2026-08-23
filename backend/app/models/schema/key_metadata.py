"""
==========================================================
AML Investigation Platform

Key Metadata

Represents a key inferred from a dataset.

Shared Across

✓ Schema Inference
✓ PostgreSQL Builder
✓ Neo4j Builder
✓ Entity Resolution
✓ Dataset Registry

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KeyMetadata:
    """
    Represents one inferred key.
    """

    # ======================================================
    # Column Information
    # ======================================================

    column_name: str

    # PRIMARY
    # FOREIGN
    # CANDIDATE
    # NATURAL
    # SURROGATE
    key_type: str

    # ======================================================
    # Confidence
    # ======================================================

    confidence: float = 0.0

    inferred: bool = True

    # ======================================================
    # Foreign Key Information
    # ======================================================

    referenced_table: str | None = None

    referenced_column: str | None = None

    # ======================================================
    # Composite Keys
    # ======================================================

    composite: bool = False

    composite_columns: list[str] = field(
        default_factory=list
    )

    # ======================================================
    # Detection Information
    # ======================================================

    reasons: list[str] = field(
        default_factory=list
    )

    # ======================================================
    # Validation
    # ======================================================

    valid: bool = True

    validation_errors: list[str] = field(
        default_factory=list
    )

    validation_warnings: list[str] = field(
        default_factory=list
    )

    # ======================================================
    # Helper Methods
    # ======================================================

    @property
    def is_primary(self) -> bool:
        return self.key_type.upper() == "PRIMARY"

    @property
    def is_foreign(self) -> bool:
        return self.key_type.upper() == "FOREIGN"

    @property
    def is_candidate(self) -> bool:
        return self.key_type.upper() == "CANDIDATE"

    @property
    def is_natural(self) -> bool:
        return self.key_type.upper() == "NATURAL"

    @property
    def is_surrogate(self) -> bool:
        return self.key_type.upper() == "SURROGATE"

    def add_reason(self, reason: str) -> None:
        if reason not in self.reasons:
            self.reasons.append(reason)

    def to_dict(self) -> dict:
        return {
            "column_name": self.column_name,
            "key_type": self.key_type,
            "confidence": self.confidence,
            "inferred": self.inferred,
            "referenced_table": self.referenced_table,
            "referenced_column": self.referenced_column,
            "composite": self.composite,
            "composite_columns": self.composite_columns,
            "reasons": self.reasons,
            "valid": self.valid,
            "validation_errors": self.validation_errors,
            "validation_warnings": self.validation_warnings,
        }