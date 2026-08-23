"""
==========================================================
AML Investigation Platform

Graph Entity Extractor

Responsibilities
----------------
✓ Read business rows
✓ Convert rows into EntityMetadata
✓ Keep graph generation generic

==========================================================
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.graph.graph_entity_mapper import GraphEntityMapper


class GraphEntityExtractor:

    def __init__(self, db: Session):

        self._db = db

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def extract(
        self,
        *,
        table_name: str,
        node_label: str,
        identifier_property: str,
    ):

        query = text(
            f"""
            SELECT *
            FROM {table_name}
            """
        )

        result = self._db.execute(query)

        entities = []

        for row in result.mappings():

            entity = GraphEntityMapper.map_row(

                node_label=node_label,

                identifier_property=identifier_property,

                row=dict(row),

                source_table=table_name,

            )

            entities.append(entity)

        return entities