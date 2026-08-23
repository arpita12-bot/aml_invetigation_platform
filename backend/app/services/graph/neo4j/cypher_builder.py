"""
==========================================================
AML Investigation Platform

Cypher Builder

Responsibilities
----------------
✓ Build Cypher for node loading
✓ Build Cypher for relationship loading
✓ Keep Neo4j queries reusable

==========================================================
"""

from __future__ import annotations


class CypherBuilder:
    """
    Generates reusable Cypher queries.
    """

    @staticmethod
    def merge_nodes(
        *,
        label: str,
        identifier_property: str,
    ) -> str:
        """
        Build Cypher for batch node loading.

        identifier_property is typically "label".
        """

        return f"""
        UNWIND $rows AS row

        MERGE (n:{label} {{
            {identifier_property}: row.{identifier_property}
        }})

        SET n += row
        """

    @staticmethod
    def merge_relationships(
        *,
        source_label: str,
        target_label: str,
        relationship_type: str,
        source_identifier: str,
        target_identifier: str,
    ) -> str:
        """
        Build Cypher for batch relationship loading.
        """

        return f"""
        UNWIND $rows AS row

        MATCH (source:{source_label} {{
            {source_identifier}: row.source_id
        }})

        MATCH (target:{target_label} {{
            {target_identifier}: row.target_id
        }})

        MERGE (source)-[r:{relationship_type}]->(target)

        SET r += row.properties
        """