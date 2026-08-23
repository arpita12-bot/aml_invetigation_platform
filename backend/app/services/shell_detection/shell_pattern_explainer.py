"""
==========================================================
AML Investigation Platform

Shell Pattern Explainer

Responsibilities
----------------
✓ Generate investigation explanations
✓ Explain shell company suspicion
✓ Produce investigation summary

==========================================================
"""

from __future__ import annotations

from app.models.shell_candidate import ShellCandidate

from app.services.shell_detection.shell_pattern_constants import (
    VERY_HIGH_RISK,
    HIGH_RISK,
    MEDIUM_RISK,
)


class ShellPatternExplainer:
    """
    Produces explainable AML investigation reports.
    """

    def explain(
        self,
        candidate: ShellCandidate,
    ) -> ShellCandidate:

        explanation = []

        explanation.append(
            self._overall_risk(candidate)
        )

        explanation.extend(
            self._community(candidate)
        )

        explanation.extend(
            self._centrality(candidate)
        )

        explanation.extend(
            self._similarity(candidate)
        )

        explanation.extend(
            self._ownership(candidate)
        )

        explanation.extend(
            self._prediction(candidate)
        )

        explanation.extend(
            self._pep(candidate)
        )

        explanation.extend(
            self._sanction(candidate)
        )

        if candidate.evidence:

            explanation.append("")

            explanation.append(
                "Supporting Evidence:"
            )

            for item in candidate.evidence:

                explanation.append(f"• {item}")

        candidate.explanation = "\n".join(explanation)

        return candidate

    # ======================================================
    # Overall Risk
    # ======================================================

    @staticmethod
    def _overall_risk(
        candidate: ShellCandidate,
    ) -> str:

        score = candidate.suspicion_score

        if score >= VERY_HIGH_RISK:

            return (
                f"Overall Assessment: VERY HIGH "
                f"shell company suspicion "
                f"(Score: {score:.2f})"
            )

        if score >= HIGH_RISK:

            return (
                f"Overall Assessment: HIGH "
                f"shell company suspicion "
                f"(Score: {score:.2f})"
            )

        if score >= MEDIUM_RISK:

            return (
                f"Overall Assessment: MEDIUM "
                f"shell company suspicion "
                f"(Score: {score:.2f})"
            )

        return (
            f"Overall Assessment: LOW "
            f"shell company suspicion "
            f"(Score: {score:.2f})"
        )

    # ======================================================
    # Community
    # ======================================================

    @staticmethod
    def _community(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.community_score == 0:
            return []

        return [

            f"Community Risk Score : "
            f"{candidate.community_score:.2f}",

            "Entity belongs to a suspicious graph community.",

        ]

    # ======================================================
    # Centrality
    # ======================================================

    @staticmethod
    def _centrality(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.centrality_score < 0.40:

            return []

        return [

            f"Centrality Score : "
            f"{candidate.centrality_score:.2f}",

            "Entity occupies an influential position "
            "within the transaction network.",

        ]

    # ======================================================
    # Similarity
    # ======================================================

    @staticmethod
    def _similarity(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.similarity_score < 0.50:

            return []

        return [

            f"Similarity Score : "
            f"{candidate.similarity_score:.2f}",

            "Highly similar to previously suspicious entities.",

        ]

    # ======================================================
    # Ownership
    # ======================================================

    @staticmethod
    def _ownership(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.ownership_score < 0.40:

            return []

        return [

            f"Ownership Score : "
            f"{candidate.ownership_score:.2f}",

            "Complex multi-layer ownership structure detected.",

        ]

    # ======================================================
    # Link Prediction
    # ======================================================

    @staticmethod
    def _prediction(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.prediction_score < 0.50:

            return []

        return [

            f"Link Prediction Score : "
            f"{candidate.prediction_score:.2f}",

            "Knowledge graph predicts hidden relationships.",

        ]

    # ======================================================
    # PEP
    # ======================================================

    @staticmethod
    def _pep(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.pep_score == 0:

            return []

        return [

            f"PEP Exposure Score : "
            f"{candidate.pep_score:.2f}",

            "Connected to one or more Politically Exposed Persons.",

        ]

    # ======================================================
    # Sanction
    # ======================================================

    @staticmethod
    def _sanction(
        candidate: ShellCandidate,
    ) -> list[str]:

        if candidate.sanction_score == 0:

            return []

        return [

            f"Sanction Exposure Score : "
            f"{candidate.sanction_score:.2f}",

            "Connected to sanctioned entities or watchlists.",

        ]