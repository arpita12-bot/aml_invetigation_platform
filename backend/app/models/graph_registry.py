"""
==========================================================
AML Investigation Platform

Graph Registry Model

Responsibilities
----------------
✓ Stores graph metadata for uploaded datasets
✓ Defines Neo4j node labels
✓ Defines identifier columns
✓ Enables dynamic graph generation

==========================================================
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    func,
)

from app.database.base import Base


class GraphRegistry(Base):
    __tablename__ = "graph_registry"

    graph_registry_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    table_name = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    node_label = Column(
        String(100),
        nullable=False,
    )

    identifier_column = Column(
        String(100),
        nullable=False,
    )

    display_column = Column(
        String(100),
        nullable=True,
    )

    entity_type = Column(
        String(100),
        nullable=True,
    )

    include_in_graph = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )