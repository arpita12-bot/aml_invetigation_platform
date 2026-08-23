"""
==========================================================
AML Investigation Platform

Path Analytics Repository

Responsibilities
----------------
✓ Execute Neo4j shortest path algorithms
✓ Discover AML investigation paths
✓ Materialize investigation intelligence

==========================================================
"""

from __future__ import annotations

from typing import Any

from neo4j import Driver
from neo4j.exceptions import Neo4jError

from app.services.graph_gds.projection.path.path_constants import (
    DEFAULT_MAX_DEPTH,
)


class PathRepository:

    """
    Repository responsible for
    graph traversal analytics.
    """

    def __init__(
        self,
        driver: Driver,
    ):

        self._driver = driver