"""
==========================================================
AML Investigation Platform

Shell Company Detector

Responsibilities
----------------
✓ Detect shell company indicators
✓ Calculate shell company score
✓ Produce explainable assessment

==========================================================
"""

from __future__ import annotations

from app.models.aml.shell_company_assessment import (
    ShellCompanyAssessment,
)
from app.models.prediction.prediction_candidate import (
    PredictionCandidate,
)


class ShellCompanyDetector:
    """
    Calculates the likelihood that a company behaves
    like a shell company.
    """

    # --------------------------------------------------
    # Indicator Weights
    # --------------------------------------------------

    LINK_WEIGHT = 0.25

    DIRECTOR_WEIGHT = 0.20

    ADDRESS_WEIGHT = 0.15

    PHONE_WEIGHT = 0.10

    DEVICE_WEIGHT = 0.10

    CIRCULAR_WEIGHT = 0.10

    REGISTRATION_WEIGHT = 0.05

    COMMUNITY_WEIGHT = 0.05

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def assess(
        self,
        *,
        prediction: PredictionCandidate,
        shared_directors: int,
        shared_addresses: int,
        shared_phone_numbers: int,
        shared_devices: int,
        circular_transactions: int,
        recent_registration: bool,
        community_score: float,
    ) -> ShellCompanyAssessment:
        """
        Calculate the shell company score.

        All numeric inputs except counts should be
        normalized to the range [0, 100].
        """

        prediction_score = prediction.confidence * 100

        director_score = min(shared_directors * 20, 100)

        address_score = min(shared_addresses * 50, 100)

        phone_score = min(shared_phone_numbers * 50, 100)

        device_score = min(shared_devices * 50, 100)

        circular_score = min(circular_transactions * 20, 100)

        registration_score = (
            100 if recent_registration else 0
        )

        total = (

            prediction_score * self.LINK_WEIGHT

            + director_score * self.DIRECTOR_WEIGHT

            + address_score * self.ADDRESS_WEIGHT

            + phone_score * self.PHONE_WEIGHT

            + device_score * self.DEVICE_WEIGHT

            + circular_score * self.CIRCULAR_WEIGHT

            + registration_score * self.REGISTRATION_WEIGHT

            + community_score * self.COMMUNITY_WEIGHT

        )

        return ShellCompanyAssessment(

            shell_score=round(total, 2),

            shared_directors=shared_directors,

            shared_addresses=shared_addresses,

            shared_phone_numbers=shared_phone_numbers,

            shared_devices=shared_devices,

            circular_transactions=circular_transactions,

            recent_registration=recent_registration,

            recommendation=self._recommendation(total),
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _recommendation(score: float) -> str:

        if score >= 85:
            return (
                "Very High likelihood of shell company. "
                "Immediate investigation recommended."
            )

        if score >= 70:
            return (
                "High likelihood of shell company. "
                "Enhanced due diligence recommended."
            )

        if score >= 50:
            return (
                "Moderate shell company indicators. "
                "Manual review recommended."
            )

        return (
            "Low shell company indicators."
        )