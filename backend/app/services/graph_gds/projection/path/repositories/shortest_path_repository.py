"""
==========================================================
AML Investigation Platform

Shortest Path Repository

Responsibilities
----------------
✓ Find shortest path between two entities
✓ Find multiple shortest paths
✓ Check path existence
✓ Execute graph traversal queries

==========================================================
"""

from __future__ import annotations

from typing import Any

from neo4j import Driver
from neo4j.exceptions import Neo4jError


class ShortestPathRepository:

    """
    Repository responsible for generic
    graph traversal operations.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver

    # ---------------------------------------------------------
    # Public Methods
    # ---------------------------------------------------------

    def find_shortest_path(

        self,

        source_id: str,

        target_id: str,

        max_depth: int = 6,

    ) -> list[dict[str, Any]]:

        query = """
        MATCH (source {entity_id:$source_id})
        MATCH (target {entity_id:$target_id})

        MATCH path = shortestPath(

            (source)-[*..$max_depth]-(target)

        )

        RETURN

            nodes(path) AS nodes,

            relationships(path) AS relationships,

            length(path) AS distance
        """

        return self._execute_query(

            query,

            source_id=source_id,

            target_id=target_id,

            max_depth=max_depth,

        )

    def find_all_shortest_paths(

        self,

        source_id: str,

        target_id: str,

        max_depth: int = 6,

    ) -> list[dict[str, Any]]:

        query = """
        MATCH (source {entity_id:$source_id})
        MATCH (target {entity_id:$target_id})

        MATCH path = allShortestPaths(

            (source)-[*..$max_depth]-(target)

        )

        RETURN

            nodes(path) AS nodes,

            relationships(path) AS relationships,

            length(path) AS distance
        """

        return self._execute_query(

            query,

            source_id=source_id,

            target_id=target_id,

            max_depth=max_depth,

        )

    def path_exists(

        self,

        source_id: str,

        target_id: str,

        max_depth: int = 6,

    ) -> bool:

        query = """
        MATCH (source {entity_id:$source_id})
        MATCH (target {entity_id:$target_id})

        MATCH path=(source)-[*..$max_depth]-(target)

        RETURN COUNT(path) > 0 AS exists
        """

        records = self._execute_query(

            query,

            source_id=source_id,

            target_id=target_id,

            max_depth=max_depth,

        )

        if not records:

            return False

        return bool(records[0]["exists"])

    # ---------------------------------------------------------
    # Internal Helper
    # ---------------------------------------------------------

    def _execute_query(

        self,

        query: str,

        **parameters,

    ) -> list[dict[str, Any]]:

        try:

            with self._driver.session() as session:

                result = session.run(

                    query,

                    **parameters,

                )

                return [

                    record.data()

                    for record in result

                ]

        except Neo4jError as exc:

            raise RuntimeError(

                "Shortest path query failed."

            ) from exc