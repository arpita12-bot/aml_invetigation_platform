"""
==========================================================
AML Investigation Platform

Cycle Analyzer

Responsibilities
----------------
✓ Detect circular relationships
✓ Produce RiskFactor objects

==========================================================
"""

from __future__ import annotations

from collections import defaultdict

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor
from app.services.risk.analyzers.base_analyzer import BaseAnalyzer


class CycleAnalyzer(BaseAnalyzer):

    MAX_DEPTH = 10

    @classmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:

        adjacency: dict[str, set[str]] = defaultdict(set)

        for relationship in graph.relationships:
            adjacency[
                relationship.source_identifier_value
            ].add(
                relationship.target_identifier_value
            )

        visited = set()
        stack = set()

        factors: list[RiskFactor] = []

        def dfs(node: str):

            visited.add(node)
            stack.add(node)

            for neighbour in adjacency.get(node, set()):

                if neighbour not in visited:
                    dfs(neighbour)

                elif neighbour in stack:

                    factors.append(

                        RiskFactor(

                            name="Circular Relationship",

                            score=90,

                            weight=0.30,

                            description=(
                                f"Cycle detected involving entity "
                                f"{neighbour}."
                            ),

                            entity_identifier=neighbour,

                        )

                    )

            stack.remove(node)

        for node in adjacency:

            if node not in visited:
                dfs(node)

        return factors