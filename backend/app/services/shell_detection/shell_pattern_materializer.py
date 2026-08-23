"""
==========================================================
AML Investigation Platform

Shell Pattern Materializer

Responsibilities
----------------
✓ Build investigation graph
✓ Score shell company candidates
✓ Generate explanations
✓ Persist investigation results
✓ Return materialization summary

==========================================================
"""

from __future__ import annotations

import time

from app.models.investigation.investigation_scope import (
    InvestigationScope,
)

from app.models.shell_materialization_result import (
    ShellMaterializationResult,
)

from app.models.shell_pattern_result import (
    ShellPatternResult,
)

from app.services.shell_detection.shell_pattern_repository import (
    ShellPatternRepository,
)

from app.services.shell_detection.shell_pattern_scoring import (
    ShellPatternScoring,
)

from app.services.shell_detection.shell_pattern_explainer import (
    ShellPatternExplainer,
)


class ShellPatternMaterializer:
    """
    Materializes shell company investigation results.

    This service orchestrates:

    Repository
        ↓
    InvestigationGraph
        ↓
    Scoring
        ↓
    Explainability
        ↓
    Persistence
        ↓
    ShellMaterializationResult
    """

    def __init__(
        self,
        repository: ShellPatternRepository,
        scoring: ShellPatternScoring,
        explainer: ShellPatternExplainer,
    ):

        self._repository = repository
        self._scoring = scoring
        self._explainer = explainer

    # =====================================================
    # Public API
    # =====================================================

    def execute(
        self,
        scope: InvestigationScope,
    ) -> ShellMaterializationResult:
        """
        Execute shell company detection
        for a single investigation scope.
        """

        start = time.perf_counter()

        # -------------------------------------------------
        # Build Investigation Graph
        # -------------------------------------------------

        graph = self._repository.build_investigation_graph(
            scope=scope,
        )

        candidates = graph.shell_candidates

        results = []
        warnings: list[str] = []
        errors: list[str] = []

        # -------------------------------------------------
        # Score & Explain Candidates
        # -------------------------------------------------

        for candidate in candidates:

            try:

                scored_candidate = self._scoring.score(
                    candidate
                )

                explained_candidate = (
                    self._explainer.explain(
                        scored_candidate
                    )
                )

                results.append(
                    explained_candidate
                )

            except Exception as exc:

                errors.append(str(exc))

        # -------------------------------------------------
        # Rank Candidates
        # -------------------------------------------------

        results.sort(
            key=lambda candidate: candidate.suspicion_score,
            reverse=True,
        )

        # -------------------------------------------------
        # Persist Results
        # -------------------------------------------------

        persisted = self._repository.save_candidates(
            results,
        )

        # -------------------------------------------------
        # Update Investigation Graph
        # -------------------------------------------------

        graph.shell_candidates = results

        # -------------------------------------------------
        # Build Shell Result
        # -------------------------------------------------

        shell_result = ShellPatternResult(

            candidates=results,

            execution_time_seconds=round(

                time.perf_counter() - start,

                3,

            ),

            successful=len(errors) == 0,

            total_candidates=persisted,

            warnings=warnings,

            errors=errors,

        )

        # -------------------------------------------------
        # Return Materialization Result
        # -------------------------------------------------

        return ShellMaterializationResult(

            investigation_graph=graph,

            shell_result=shell_result,

        )