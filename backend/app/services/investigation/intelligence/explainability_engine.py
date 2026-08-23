"""
==========================================================
AML Investigation Platform

Explainability Engine

==========================================================
"""

from __future__ import annotations

from app.models.investigation.investigation_context import (
    InvestigationContext,
)


class ExplainabilityEngine:

    """
    Converts investigation evidence into
    investigator-readable explanations.
    """

    def build(
        self,
        context: InvestigationContext,
    ) -> list[str]:

        explanations: list[str] = []

        # ----------------------------------------------

        if context.path_result:

            if context.path_result.paths:

                explanations.append(

                    f"{len(context.path_result.paths)} "
                    "suspicious graph paths identified."

                )

        # ----------------------------------------------

        if getattr(context, "centrality_metrics", None):

            metric = context.centrality_metrics[0]

            explanations.append(

                "Entity has high influence in the "
                f"network (PageRank "
                f"{metric.page_rank:.3f})."

            )

        # ----------------------------------------------

        if getattr(context, "community_metrics", None):

            community = context.community_metrics[0]

            explanations.append(

                "Entity belongs to community "

                f"{community.louvain_community} "

                f"with "

                f"{community.community_size} members."

            )

        # ----------------------------------------------

        if getattr(context, "similarity_metrics", None):

            similarity = context.similarity_metrics[0]

            explanations.append(

                "Behavior is highly similar "

                f"({similarity.score:.2f}) "

                "to other investigated entities."

            )

        # ----------------------------------------------

        if context.shell_result:

            if context.shell_result.shell_companies_found:

                explanations.append(

                    "Shell company pattern detected."

                )

        return explanations