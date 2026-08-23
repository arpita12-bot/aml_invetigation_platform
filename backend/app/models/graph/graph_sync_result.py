"""
==========================================================
AML Investigation Platform

Graph Sync Result

Represents the result of one Neo4j synchronization.

Shared Across

✓ Graph Loader
✓ Graph Sync Service
✓ Dashboard
✓ Audit Logs
✓ Monitoring
✓ Performance Metrics

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class GraphSyncResult:
    """
    Result of a graph synchronization operation.
    """

    # =====================================================
    # Graph
    # =====================================================

    graph_name: str

    # =====================================================
    # Loading Statistics
    # =====================================================

    nodes_loaded: int = 0

    relationships_loaded: int = 0

    constraints_created: int = 0

    indexes_created: int = 0

    # =====================================================
    # Execution
    # =====================================================

    execution_time_seconds: float = 0.0

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # =====================================================
    # Status
    # =====================================================

    success: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def total_nodes(self) -> int:
        return self.nodes_loaded

    @property
    def total_relationships(self) -> int:
        return self.relationships_loaded

    @property
    def total_objects(self) -> int:
        return (
            self.nodes_loaded
            + self.relationships_loaded
        )

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def is_successful(self) -> bool:
        return (
            self.success
            and not self.has_errors
        )

    def to_dict(self) -> dict:
        """
        Convert the synchronization result into
        a serializable dictionary.
        """

        return {

            "graph_name": self.graph_name,

            "nodes_loaded": self.nodes_loaded,

            "relationships_loaded":
                self.relationships_loaded,

            "constraints_created":
                self.constraints_created,

            "indexes_created":
                self.indexes_created,

            "execution_time_seconds":
                self.execution_time_seconds,

            "started_at":
                self.started_at.isoformat()
                if self.started_at
                else None,

            "finished_at":
                self.finished_at.isoformat()
                if self.finished_at
                else None,

            "success":
                self.success,

            "errors":
                self.errors,

            "warnings":
                self.warnings,

            "total_nodes":
                self.total_nodes,

            "total_relationships":
                self.total_relationships,

            "total_objects":
                self.total_objects,
        }