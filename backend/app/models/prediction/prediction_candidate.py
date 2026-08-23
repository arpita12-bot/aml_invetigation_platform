"""
==========================================================
AML Investigation Platform

Prediction Candidate

Represents one predicted entity.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PredictionCandidate:
    """
    One ranked prediction.
    """

    entity: str

    score: float

    rank: int

    entity_type: str | None = None

    confidence: float | None = None

    def to_dict(self) -> dict:

        return {

            "entity": self.entity,

            "score": self.score,

            "rank": self.rank,

            "entity_type": self.entity_type,

            "confidence": self.confidence,
        }