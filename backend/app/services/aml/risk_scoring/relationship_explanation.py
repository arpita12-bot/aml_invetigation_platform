"""
==========================================================
AML Investigation Platform

Relationship Explanation

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RelationshipExplanation:
    """
    Human-readable explanation for a predicted relationship.
    """

    confidence: float

    summary: str

    evidence: list[str] = field(default_factory=list)

    graph_features: list[str] = field(default_factory=list)

    business_rules: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:

        return {

            "confidence": self.confidence,

            "summary": self.summary,

            "evidence": self.evidence,

            "graph_features": self.graph_features,

            "business_rules": self.business_rules,

            "recommendations": self.recommendations,
        }