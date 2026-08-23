"""
==========================================================
AML Investigation Platform

Relationship Explainer

Responsibilities
----------------

✓ Explain predicted relationships
✓ Summarize graph evidence
✓ Summarize business indicators
✓ Produce investigator-friendly output

==========================================================
"""

from __future__ import annotations

from app.models.prediction.prediction_candidate import (
    PredictionCandidate,
)

from app.services.aml.risk_scoring.relationship_explanation import (
    RelationshipExplanation,
)


class RelationshipExplainer:

    """
    Generates explainable AML evidence.
    """

    def explain(
        self,
        *,
        prediction: PredictionCandidate,
        shared_directors: int,
        shared_addresses: int,
        shared_phone_numbers: int,
        shared_devices: int,
        circular_transactions: int,
        community_score: float,
    ) -> RelationshipExplanation:

        evidence = []

        graph_features = []

        business_rules = []

        recommendations = []

        # -------------------------------------
        # Identity Evidence
        # -------------------------------------

        if shared_directors:

            evidence.append(
                f"{shared_directors} shared director(s)"
            )

        if shared_addresses:

            evidence.append(
                f"{shared_addresses} shared address(es)"
            )

        if shared_phone_numbers:

            evidence.append(
                f"{shared_phone_numbers} shared phone number(s)"
            )

        if shared_devices:

            evidence.append(
                f"{shared_devices} shared device/IP(s)"
            )

        # -------------------------------------
        # Graph Evidence
        # -------------------------------------

        if circular_transactions:

            graph_features.append(
                f"{circular_transactions} circular transaction path(s)"
            )

        if community_score >= 70:

            graph_features.append(
                "Entities belong to a high-risk graph community."
            )

        if prediction.confidence >= 0.90:

            graph_features.append(
                "Very high embedding similarity."
            )

        # -------------------------------------
        # Business Rules
        # -------------------------------------

        if prediction.confidence >= 0.85:

            business_rules.append(
                "Prediction exceeds AML confidence threshold."
            )

        if shared_directors >= 2:

            business_rules.append(
                "Multiple common directors detected."
            )

        if shared_addresses >= 1:

            business_rules.append(
                "Shared registered address detected."
            )

        # -------------------------------------
        # Recommendations
        # -------------------------------------

        if prediction.confidence >= 0.90:

            recommendations.append(
                "Prioritize manual investigation."
            )

        if circular_transactions:

            recommendations.append(
                "Review transaction flow for layering."
            )

        if shared_devices:

            recommendations.append(
                "Investigate shared digital footprint."
            )

        summary = (
            "Predicted relationship supported by graph "
            "connectivity, shared identifiers, and AML "
            "business rules."
        )

        return RelationshipExplanation(

            confidence=prediction.confidence,

            summary=summary,

            evidence=evidence,

            graph_features=graph_features,

            business_rules=business_rules,

            recommendations=recommendations,
        )