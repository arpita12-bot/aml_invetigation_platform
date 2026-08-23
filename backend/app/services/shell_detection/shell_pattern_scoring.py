"""
==========================================================
AML Investigation Platform

Shell Pattern Scoring

Responsibilities
----------------
✓ Calculate suspicion score
✓ Build investigation evidence
✓ Produce ShellCandidate

==========================================================
"""

from __future__ import annotations

from app.models.shell_candidate import ShellCandidate
from app.models.shell_pattern_candidate import ShellPatternCandidate

from app.services.shell_detection.shell_pattern_constants import (
    COMMUNITY_WEIGHT,
    LINK_PREDICTION_WEIGHT,
    OWNERSHIP_WEIGHT,
    PAGERANK_WEIGHT,
    PEP_WEIGHT,
    SANCTION_WEIGHT,
    SIMILARITY_WEIGHT,
)


class ShellPatternScoring:

    """
    AML Intelligence Scoring Engine.
    """

    def score(
        self,
        candidate: ShellPatternCandidate,
    ) -> ShellCandidate:

        community_score = self._community_score(candidate)

        centrality_score = self._centrality_score(candidate)

        similarity_score = self._similarity_score(candidate)

        ownership_score = self._ownership_score(candidate)

        prediction_score = candidate.prediction_score

        pep_score = self._pep_score(candidate)

        sanction_score = self._sanction_score(candidate)

        suspicion = (

            prediction_score * LINK_PREDICTION_WEIGHT +

            similarity_score * SIMILARITY_WEIGHT +

            centrality_score * PAGERANK_WEIGHT +

            community_score * COMMUNITY_WEIGHT +

            ownership_score * OWNERSHIP_WEIGHT +

            pep_score * PEP_WEIGHT +

            sanction_score * SANCTION_WEIGHT

        )

        evidence = self._build_evidence(candidate)

        return ShellCandidate(

            company_id=candidate.company_id,

            company_name=candidate.company_name,

            suspicion_score=round(suspicion, 3),

            community_score=community_score,

            centrality_score=centrality_score,

            similarity_score=similarity_score,

            ownership_score=ownership_score,

            prediction_score=prediction_score,

            pep_score=pep_score,

            sanction_score=sanction_score,

            explanation="",

            evidence=evidence,

        )

    # =======================================================
    # Individual Scores
    # =======================================================

    @staticmethod
    def _community_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        if candidate.community_size == 0:
            return 0.0

        return min(candidate.community_size / 100.0, 1.0)

    @staticmethod
    def _centrality_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        return min(candidate.page_rank, 1.0)

    @staticmethod
    def _similarity_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        return min(candidate.similarity_score, 1.0)

    @staticmethod
    def _ownership_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        return min(candidate.ownership_layers / 6.0, 1.0)

    @staticmethod
    def _pep_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        return min(candidate.pep_connections / 5.0, 1.0)

    @staticmethod
    def _sanction_score(
        candidate: ShellPatternCandidate,
    ) -> float:

        return min(candidate.sanction_connections / 5.0, 1.0)

    # =======================================================
    # Evidence
    # =======================================================

    @staticmethod
    def _build_evidence(
        candidate: ShellPatternCandidate,
    ) -> list[str]:

        evidence = []

        if candidate.community_size > 20:
            evidence.append(
                "Large suspicious community detected."
            )

        if candidate.page_rank > 0.70:
            evidence.append(
                "High PageRank centrality."
            )

        if candidate.similarity_score > 0.80:
            evidence.append(
                "High similarity to suspicious entities."
            )

        if candidate.prediction_score > 0.80:
            evidence.append(
                "Strong link prediction confidence."
            )

        if candidate.ownership_layers >= 3:
            evidence.append(
                "Complex ownership structure."
            )

        if candidate.pep_connections > 0:
            evidence.append(
                "Connected to politically exposed persons."
            )

        if candidate.sanction_connections > 0:
            evidence.append(
                "Connected to sanctioned entities."
            )

        return evidence