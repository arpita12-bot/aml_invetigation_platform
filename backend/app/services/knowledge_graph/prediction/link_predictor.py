"""
==========================================================
AML Investigation Platform

Prediction Service

Responsibilities
----------------
✓ Validate prediction requests
✓ Execute link prediction
✓ Apply confidence filtering
✓ Log prediction requests
✓ Return prediction results

==========================================================
"""

from __future__ import annotations

import logging

from app.models.prediction.prediction_request import PredictionRequest
from app.models.prediction.prediction_result import PredictionResult
from app.services.knowledge_graph.prediction.link_predictor import (
    LinkPredictor,
)

logger = logging.getLogger(__name__)


class PredictionService:
    """
    High-level orchestration service for
    Knowledge Graph link prediction.
    """

    def __init__(
        self,
        predictor: LinkPredictor,
    ) -> None:

        self._predictor = predictor

    def predict(
        self,
        request: PredictionRequest,
    ) -> PredictionResult:
        """
        Execute a prediction request.
        """

        self._validate_request(request)

        logger.info(
            "Running prediction: relation=%s head=%s tail=%s top_k=%d",
            request.relation,
            request.head,
            request.tail,
            request.top_k,
        )

        result = self._predictor.predict(request)

        result.candidates = [
            candidate
            for candidate in result.candidates
            if (
                candidate.confidence is None
                or candidate.confidence >= request.threshold
            )
        ]

        logger.info(
            "Prediction complete. %d candidates returned.",
            len(result.candidates),
        )

        return result

    @staticmethod
    def _validate_request(
        request: PredictionRequest,
    ) -> None:

        if not request.relation:
            raise ValueError(
                "Relation is required."
            )

        if request.top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        if not (0.0 <= request.threshold <= 1.0):
            raise ValueError(
                "Threshold must be between 0 and 1."
            )

        if request.head and request.tail:
            raise ValueError(
                "Specify either head or tail, not both."
            )

        if not request.head and not request.tail:
            raise ValueError(
                "Specify either a head or a tail."
            )