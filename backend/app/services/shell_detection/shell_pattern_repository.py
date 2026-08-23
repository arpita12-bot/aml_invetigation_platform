"""
==========================================================
AML Investigation Platform

Shell Pattern Repository

Responsibilities
----------------
✓ Build investigation graph
✓ Load graph neighborhood
✓ Load shell candidates
✓ Load graph nodes
✓ Load graph relationships
✓ Persist shell analysis

==========================================================
"""

from __future__ import annotations

from typing import Any

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.models.investigation.graph_node import (
    GraphNode,
)
from app.models.investigation.graph_relationship import (
    GraphRelationship,
)
from app.models.investigation.investigation_graph import (
    InvestigationGraph,
)
from app.models.investigation.investigation_scope import (
    InvestigationScope,
)

from typing import Any

from app.models.shell_candidate import (
    ShellCandidate,
)

from app.models.shell_pattern_candidate import (
    ShellPatternCandidate,
)


class ShellPatternRepository:
    """
    Repository responsible for constructing the
    investigation graph from Neo4j.

    No business logic.
    No scoring.
    No explainability.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # =====================================================
    # Public API
    # =====================================================

    def build_investigation_graph(
        self,
        scope: InvestigationScope,
    ) -> InvestigationGraph:
        """
        Build a complete investigation graph
        around the supplied entity.
        """

        nodes = self._load_nodes(scope)

        relationships = self._load_relationships(scope)

        candidates = self._load_shell_candidates(scope)

        paths = self._load_paths(scope)

        return InvestigationGraph(

            root_entity_id=scope.entity_id,

            nodes=nodes,

            relationships=relationships,

            shell_candidates=candidates,

            paths=paths,

            metadata={

                "entity_type": scope.entity_type,

                "max_depth": scope.max_depth,

            },
        )

    # =====================================================
    # Common Query Executor
    # =====================================================

    def _execute_query(
        self,
        query: str,
        **parameters,
    ) -> list[Any]:
        """
        Execute a Neo4j query and return records.
        """

        try:

            with self._driver.session() as session:

                return list(

                    session.run(

                        query,

                        **parameters,

                    )

                )

        except Neo4jError as exc:

            raise RuntimeError(
                "Neo4j query execution failed."
            ) from exc

    # =====================================================
    # Load Investigation Nodes
    # =====================================================

    def _load_nodes(
        self,
        scope: InvestigationScope,
    ) -> list[GraphNode]:
        """
        Load all graph nodes inside the
        investigation boundary.
        """

        query = """
        MATCH (root)

        WHERE root.company_id = $entity_id

        CALL apoc.path.subgraphNodes(

            root,

            {

                relationshipFilter:

                    "OWNS>|DIRECTOR_OF>|TRANSFERRED_TO>|HAS_ACCOUNT>",

                maxLevel: $depth

            }

        )

        YIELD node

        RETURN

            id(node)            AS node_id,

            labels(node)        AS labels,

            properties(node)    AS properties
        """

        records = self._execute_query(

            query,

            entity_id=scope.entity_id,

            depth=scope.max_depth,

        )

        return self._map_nodes(records)
    
    # =====================================================
    # Load Investigation Relationships
    # =====================================================

    def _load_relationships(
        self,
        scope: InvestigationScope,
    ) -> list[GraphRelationship]:
        """
        Load all relationships inside the
        investigation boundary.
        """

        query = """
        MATCH (root)

        WHERE root.company_id = $entity_id

        CALL apoc.path.subgraphNodes(

            root,

            {

                relationshipFilter:
                    "OWNS>|DIRECTOR_OF>|TRANSFERRED_TO>|HAS_ACCOUNT>",

                maxLevel: $depth

            }

        )

        YIELD node

        WITH collect(node) AS nodes

        UNWIND nodes AS source

        MATCH (source)-[r]->(target)

        WHERE target IN nodes

        RETURN

            type(r)               AS relationship_type,

            id(source)            AS source_id,

            id(target)            AS target_id,

            properties(r)         AS properties
        """

        records = self._execute_query(

            query,

            entity_id=scope.entity_id,

            depth=scope.max_depth,

        )

        return self._map_relationships(records)

    # =====================================================
    # Load Shell Candidates
    # =====================================================

    def _load_shell_candidates(
        self,
        scope: InvestigationScope,
    ) -> list[ShellPatternCandidate]:
        """
        Load shell company candidates
        inside the investigation graph.
        """

        query = """
        MATCH (root)

        WHERE root.company_id = $entity_id

        CALL apoc.path.subgraphNodes(

            root,

            {

                relationshipFilter:
                    "OWNS>|DIRECTOR_OF>|TRANSFERRED_TO>|HAS_ACCOUNT>",

                maxLevel: $depth

            }

        )

        YIELD node

        WITH node

        WHERE node:Company

        OPTIONAL MATCH (node)-[:SIMILAR_TO]-()

        WITH

            node,

            COUNT(*) AS similarity_connections

        RETURN

            node.company_id                AS company_id,

            node.name                      AS company_name,

            node.community_id              AS community_id,

            node.community_size            AS community_size,

            node.degree_centrality         AS degree_centrality,

            node.betweenness_centrality    AS betweenness_centrality,

            node.closeness_centrality      AS closeness_centrality,

            node.page_rank                 AS page_rank,

            node.link_prediction_score     AS prediction_score,

            similarity_connections         AS similarity_score,

            node.ownership_layers          AS ownership_layers,

            node.pep_connections           AS pep_connections,

            node.sanction_connections      AS sanction_connections,

            node.transaction_count         AS suspicious_transactions,

            node.country                   AS country,

            node.industry                  AS industry

        ORDER BY

            node.page_rank DESC
        """

        records = self._execute_query(

            query,

            entity_id=scope.entity_id,

            depth=scope.max_depth,

        )

        return self._map_candidates(records)

    # =====================================================
    # Load Investigation Paths
    # =====================================================

    def _load_paths(
    self,
    scope: InvestigationScope,
    ) -> list[Any]:
        """
        Placeholder.

        Path analytics will populate this
        during PathJob execution.
        """

        return []
    
    # =====================================================
    # Mapping Methods
    # =====================================================

    def _map_nodes(
        self,
        records: list,
    ) -> list[GraphNode]:
        """
        Convert Neo4j node records into GraphNode models.
        """

        nodes: list[GraphNode] = []

        for record in records:

            labels = record["labels"] or []

            label = labels[0] if labels else "Unknown"

            nodes.append(

                GraphNode(

                    node_id=str(record["node_id"]),

                    label=label,

                    properties=record["properties"] or {},

                )

            )

        return nodes

    def _map_relationships(
        self,
        records: list,
    ) -> list[GraphRelationship]:
        """
        Convert Neo4j relationship records into
        GraphRelationship models.
        """

        relationships: list[GraphRelationship] = []

        for record in records:

            relationships.append(

                GraphRelationship(

                    relationship_type=record["relationship_type"],

                    source_id=str(record["source_id"]),

                    target_id=str(record["target_id"]),

                    properties=record["properties"] or {},

                )

            )

        return relationships

    def _map_candidates(
        self,
        records: list,
    ) -> list[ShellPatternCandidate]:
        """
        Convert Neo4j records into
        ShellPatternCandidate models.
        """

        candidates: list[ShellPatternCandidate] = []

        for record in records:

            candidate = ShellPatternCandidate(

                company_id=record["company_id"],

                company_name=record["company_name"],

                community_id=record["community_id"],

                community_size=int(
                    record["community_size"] or 0
                ),

                degree_centrality=float(
                    record["degree_centrality"] or 0.0
                ),

                betweenness_centrality=float(
                    record["betweenness_centrality"] or 0.0
                ),

                closeness_centrality=float(
                    record["closeness_centrality"] or 0.0
                ),

                page_rank=float(
                    record["page_rank"] or 0.0
                ),

                similarity_score=float(
                    record["similarity_score"] or 0.0
                ),

                prediction_score=float(
                    record["prediction_score"] or 0.0
                ),

                ownership_layers=int(
                    record["ownership_layers"] or 0
                ),

                pep_connections=int(
                    record["pep_connections"] or 0
                ),

                sanction_connections=int(
                    record["sanction_connections"] or 0
                ),

                suspicious_transactions=int(
                    record["suspicious_transactions"] or 0
                ),

                country=record["country"] or "",

                industry=record["industry"] or "",

                evidence=[],

            )

            candidates.append(candidate)

        return candidates
    
    # =====================================================
    # Utility Methods
    # =====================================================

    def count_candidates(
        self,
        scope: InvestigationScope,
    ) -> int:
        """
        Return the number of shell company candidates
        within the current investigation scope.
        """

        graph = self.build_investigation_graph(scope)

        return len(graph.shell_candidates)

    def find_candidate(
        self,
        company_id: str,
        scope: InvestigationScope,
    ) -> ShellPatternCandidate | None:
        """
        Find a candidate company inside the
        investigation graph.
        """

        graph = self.build_investigation_graph(scope)

        for candidate in graph.shell_candidates:

            if candidate.company_id == company_id:
                return candidate

        return None

    # =====================================================
    # Persistence
    # =====================================================

    def save_candidates(
        self,
        candidates: list[ShellCandidate],
    ) -> int:
        """
        Persist shell company investigation
        results back into Neo4j.
        """

        if not candidates:
            return 0

        query = """
        UNWIND $candidates AS candidate

        MATCH (company:Company {
            company_id: candidate.company_id
        })

        SET

            company.shell_suspicion_score =
                candidate.suspicion_score,

            company.shell_explanation =
                candidate.explanation,

            company.last_shell_analysis =
                datetime()
        """

        payload = []

        for candidate in candidates:

            payload.append(

                {

                    "company_id":
                        candidate.company_id,

                    "suspicion_score":
                        candidate.suspicion_score,

                    "explanation":
                        candidate.explanation,

                }

            )

        try:

            with self._driver.session() as session:

                session.run(

                    query,

                    candidates=payload,

                )

        except Neo4jError as exc:

            raise RuntimeError(
                "Failed to persist shell analysis."
            ) from exc

        return len(payload)