"""
==========================================================
AML Investigation Platform

Graph Validator

==========================================================
"""

from __future__ import annotations

from app.services.graph.neo4j.neo4j_connection import Neo4jConnection


class GraphValidator:

    REQUIRED_LABELS = [
        "Customer",
        "Account",
        "Transaction",
        "Company",
    ]

    REQUIRED_RELATIONSHIPS = [
        "HAS_ACCOUNT",
        "TRANSFERRED_TO",
    ]

    def validate(self) -> dict:

        report = {
            "labels": {},
            "relationships": {},
            "duplicates": {},
            "orphans": {},
            "missing_properties": {},
        }

        with Neo4jConnection.session() as session:

            # --------------------------------------------
            # Labels
            # --------------------------------------------

            for label in self.REQUIRED_LABELS:

                query = f"""
                MATCH (n:{label})
                RETURN count(n) AS count
                """

                count = session.run(query).single()["count"]

                report["labels"][label] = count

            # --------------------------------------------
            # Relationships
            # --------------------------------------------

            for rel in self.REQUIRED_RELATIONSHIPS:

                query = f"""
                MATCH ()-[r:{rel}]->()
                RETURN count(r) AS count
                """

                count = session.run(query).single()["count"]

                report["relationships"][rel] = count

            # --------------------------------------------
            # Duplicate Customers
            # --------------------------------------------

            query = """
            MATCH (c:Customer)
            WITH c.customer_id AS id, count(*) AS cnt
            WHERE cnt > 1
            RETURN count(*) AS duplicates
            """

            report["duplicates"]["Customer"] = (
                session.run(query).single()["duplicates"]
            )

            # --------------------------------------------
            # Orphan Accounts
            # --------------------------------------------

            query = """
            MATCH (a:Account)
            WHERE NOT (a)<-[:HAS_ACCOUNT]-(:Customer)
            RETURN count(a) AS count
            """

            report["orphans"]["Account"] = (
                session.run(query).single()["count"]
            )

        return report