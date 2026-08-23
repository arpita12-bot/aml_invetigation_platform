"""
==========================================================
AML Investigation Platform

Semantic Metadata

Represents inferred business semantics
for a dataset column.

Shared Across

✓ Schema Inference
✓ PostgreSQL Builder
✓ Neo4j Builder
✓ Entity Resolution
✓ Knowledge Graph
✓ Feature Engineering

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SemanticMetadata:
    """
    Represents semantic meaning inferred
    for a dataset column.
    """

    # =====================================================
    # Semantic Information
    # =====================================================

    semantic_type: str

    confidence: float = 0.0

    inferred: bool = True

    # =====================================================
    # Detection
    # =====================================================

    matched_alias: str | None = None

    detection_method: str = "PATTERN"

    evidence: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Validation
    # =====================================================

    valid: bool = True

    validation_errors: list[str] = field(
        default_factory=list
    )

    validation_warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    def add_evidence(
        self,
        reason: str,
    ) -> None:

        if reason not in self.evidence:

            self.evidence.append(reason)

    def to_dict(self) -> dict:

        return {

            "semantic_type": self.semantic_type,

            "confidence": self.confidence,

            "inferred": self.inferred,

            "matched_alias": self.matched_alias,

            "detection_method": self.detection_method,

            "evidence": self.evidence,

            "valid": self.valid,

            "validation_errors": self.validation_errors,

            "validation_warnings": self.validation_warnings,

        }