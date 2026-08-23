"""
==========================================================
AML Investigation Platform

Graph Projection Repository

Responsibilities
----------------
✓ Execute Neo4j GDS procedures
✓ Manage graph projections
✓ Return projection metadata

==========================================================
"""

from __future__ import annotations

from neo4j import Driver

from app.models.graph_gds.graph_projection import GraphProjection


class GraphProjectionRepository:
    """
    Repository responsible for managing Neo4j
    Graph Data Science projections.
    """

    def __init__(self, driver: Driver):

        self._driver = driver

    # -----------------------------------------------------
    # Projection Exists
    # -----------------------------------------------------

    def projection_exists(
        self,
        graph_name: str,
    ) -> bool:

        query = """
        CALL gds.graph.exists($graph_name)
        YIELD exists
        RETURN exists
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                graph_name=graph_name,

            ).single()

        return bool(record["exists"]) if record else False

    # -----------------------------------------------------
    # Create Projection
    # -----------------------------------------------------

    def create_projection(
        self,
        graph_name: str,
        node_labels: list[str],
        relationship_types: list[str],
    ) -> GraphProjection:

        query = """
        CALL gds.graph.project(
            $graph_name,
            $node_labels,
            $relationship_types
        )
        YIELD
            graphName,
            nodeCount,
            relationshipCount
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                graph_name=graph_name,

                node_labels=node_labels,

                relationship_types=relationship_types,

            ).single()

        return GraphProjection(

            graph_name=record["graphName"],

            node_count=record["nodeCount"],

            relationship_count=record["relationshipCount"],

            node_labels=node_labels,

            relationship_types=relationship_types,

            exists=True,
        )

    # -----------------------------------------------------
    # Drop Projection
    # -----------------------------------------------------

    def drop_projection(
        self,
        graph_name: str,
    ) -> bool:

        query = """
        CALL gds.graph.drop($graph_name, false)
        YIELD graphName
        """

        with self._driver.session() as session:

            result = session.run(

                query,

                graph_name=graph_name,

            ).single()

        return result is not None

    # -----------------------------------------------------
    # Projection Info
    # -----------------------------------------------------

    def projection_info(
        self,
        graph_name: str,
    ) -> GraphProjection | None:

        query = """
        CALL gds.graph.list($graph_name)

        YIELD

            graphName,

            nodeCount,

            relationshipCount,

            schema

        RETURN

            graphName,

            nodeCount,

            relationshipCount,

            schema
        """

        with self._driver.session() as session:

            record = session.run(

                query,

                graph_name=graph_name,

            ).single()

        if record is None:

            return None

        schema = record["schema"]

        return GraphProjection(

            graph_name=record["graphName"],

            node_count=record["nodeCount"],

            relationship_count=record["relationshipCount"],

            node_labels=list(schema["nodes"].keys()),

            relationship_types=list(schema["relationships"].keys()),

            exists=True,
        )

    # -----------------------------------------------------
    # List All Projections
    # -----------------------------------------------------

    def list_projections(
        self,
    ) -> list[GraphProjection]:

        query = """
        CALL gds.graph.list()

        YIELD

            graphName,

            nodeCount,

            relationshipCount,

            schema

        RETURN

            graphName,

            nodeCount,

            relationshipCount,

            schema

        ORDER BY graphName
        """

        projections: list[GraphProjection] = []

        with self._driver.session() as session:

            result = session.run(query)

            for record in result:

                schema = record["schema"]

                projections.append(

                    GraphProjection(

                        graph_name=record["graphName"],

                        node_count=record["nodeCount"],

                        relationship_count=record["relationshipCount"],

                        node_labels=list(schema["nodes"].keys()),

                        relationship_types=list(
                            schema["relationships"].keys()
                        ),

                        exists=True,
                    )

                )

        return projections