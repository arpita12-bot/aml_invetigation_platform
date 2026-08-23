"""
==========================================================
AML Investigation Platform

Graph Statistics Service

==========================================================
"""

from __future__ import annotations

from app.services.graph.neo4j.neo4j_connection import Neo4jConnection


class GraphStatisticsService:

    def generate(self) -> dict:

        with Neo4jConnection.session() as session:

            total_nodes = session.run(
                """
                MATCH (n)
                RETURN count(n) AS total
                """
            ).single()["total"]

            total_relationships = session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS total
                """
            ).single()["total"]

            labels = {}

            result = session.run(
                """
                CALL db.labels()
                """
            )

            for row in result:

                label = row["label"]

                count = session.run(
                    f"""
                    MATCH (n:{label})
                    RETURN count(n) AS total
                    """
                ).single()["total"]

                labels[label] = count

            relationship_types = {}

            result = session.run(
                """
                CALL db.relationshipTypes()
                """
            )

            for row in result:

                rel = row["relationshipType"]

                count = session.run(
                    f"""
                    MATCH ()-[r:{rel}]->()
                    RETURN count(r) AS total
                    """
                ).single()["total"]

                relationship_types[rel] = count

            density = 0

            if total_nodes > 1:
                density = (
                    total_relationships
                    / (total_nodes * (total_nodes - 1))
                )

            return {
                "total_nodes": total_nodes,
                "total_relationships": total_relationships,
                "labels": labels,
                "relationship_types": relationship_types,
                "density": density,
            }