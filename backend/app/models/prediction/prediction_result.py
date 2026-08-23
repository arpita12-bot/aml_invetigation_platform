"""
==========================================================
AML Investigation Platform

Prediction Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.prediction.prediction_candidate import (
    PredictionCandidate,
)


@dataclass(slots=True)
class PredictionResult:

    query: str

    candidates: list[PredictionCandidate] = field(
        default_factory=list
    )

    execution_time_seconds: float = 0.0

    errors: list[str] = field(
        default_factory=list
    )

    @property
    def total_predictions(self) -> int:

        return len(self.candidates)