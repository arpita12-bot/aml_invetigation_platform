"""
==========================================================
AML Investigation Platform

Risk Scoring Service

Responsibilities
----------------
✓ Calculate AML risk score
✓ Combine multiple risk indicators
✓ Assign risk level
✓ Produce explainable results

==========================================================
"""

from __future__ import annotations

from app.models.aml.risk_score import RiskScore
from app.models.prediction.prediction_candidate import (
    PredictionCandidate,
)


class RiskScoringService:
    """
    Calculates the overall AML risk score for a
    predicted relationship.
    """

    # --------------------------------------------------
    # Weights
    # --------------------------------------------------

    PREDICTION_WEIGHT = 0.35

    CUSTOMER_WEIGHT = 0.20

    COMPANY_WEIGHT = 0.20

    GRAPH_WEIGHT = 0.15

    TRANSACTION_WEIGHT = 0.10

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def calculate(
        self,
        *,
        prediction: PredictionCandidate,
        customer_score: float,
        company_score: float,
        graph_score: float,
        transaction_score: float,
    ) -> RiskScore:
        """
        Calculate a weighted AML risk score.

        All component scores should be normalized
        to the range [0, 100].
        """

        prediction_score = prediction.confidence * 100

        total = (

            prediction_score
            * self.PREDICTION_WEIGHT

            + customer_score
            * self.CUSTOMER_WEIGHT

            + company_score
            * self.COMPANY_WEIGHT

            + graph_score
            * self.GRAPH_WEIGHT

            + transaction_score
            * self.TRANSACTION_WEIGHT

        )

        risk_level = self._risk_level(total)

        return RiskScore(

            total_score=round(total, 2),

            prediction_score=round(
                prediction_score,
                2,
            ),

            graph_score=round(
                graph_score,
                2,
            ),

            customer_score=round(
                customer_score,
                2,
            ),

            company_score=round(
                company_score,
                2,
            ),

            transaction_score=round(
                transaction_score,
                2,
            ),

            risk_level=risk_level,

            confidence=prediction.confidence,
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _risk_level(score: float) -> str:

        if score >= 85:
            return "CRITICAL"

        if score >= 70:
            return "HIGH"

        if score >= 50:
            return "MEDIUM"

        return "LOW"