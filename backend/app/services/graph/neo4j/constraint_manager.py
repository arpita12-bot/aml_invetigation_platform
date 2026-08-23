"""
==========================================================
AML Investigation Platform

Neo4j Constraint Manager

Responsibilities
----------------
✓ Create node constraints
✓ Create indexes
✓ Ensure idempotent schema creation

==========================================================
"""

from __future__ import annotations

from app.models.graph.graph_metadata import GraphMetadata


class ConstraintManager:
    """
    Manages Neo4j schema objects.
    """

    @classmethod
    def create_constraints(
        cls,
        session,
        graph: GraphMetadata,
    ) -> int:
        """
        Create uniqueness constraints for all node labels.
        """

        labels = {
            entity.node_label
            for entity in graph.entities
        }

        created = 0

        for label in labels:

            cypher = f"""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (n:{label})
            REQUIRE n.label IS UNIQUE
            """

            session.run(cypher)

            created += 1

        return created

    @classmethod
    def create_indexes(
        cls,
        session,
        graph: GraphMetadata,
    ) -> int:
        """
        Create indexes for frequently queried node labels.
        """

        labels = {
            entity.node_label
            for entity in graph.entities
        }

        created = 0

        for label in labels:

            cypher = f"""
            CREATE INDEX IF NOT EXISTS
            FOR (n:{label})
            ON (n.label)
            """

            session.run(cypher)

            created += 1

        return created