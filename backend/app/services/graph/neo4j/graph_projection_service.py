"""
==========================================================
AML Investigation Platform

Graph Projection Service

Responsibilities
----------------
✓ Refresh Neo4j GDS projections
✓ Create graph projections
✓ Drop existing projections if needed
==========================================================
"""

from app.services.graph.neo4j.neo4j_connection import Neo4jConnection


class GraphProjectionService:

    GRAPH_NAME = "aml_graph"

    @classmethod
    def refresh_projection(cls) -> None:
        """
        Refresh the GDS projection.

        Safe to call even if GDS is not installed.
        """
        try:
            with Neo4jConnection().session() as session:

                session.run(
                    f"""
                    CALL gds.graph.drop('{cls.GRAPH_NAME}', false)
                    """
                )

                session.run(
                    f"""
                    CALL gds.graph.project(
                        '{cls.GRAPH_NAME}',
                        '*',
                        '*'
                    )
                    """
                )

        except Exception:
            # Ignore projection failures so ingestion succeeds.
            pass