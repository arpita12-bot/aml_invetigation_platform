"""
==========================================================
AML Investigation Platform

Path Analytics Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.graph_gds.path_result import (
    GraphPath,
)


@dataclass(slots=True)
class PathJobResult:
    """
    Aggregated result returned by PathJob.
    """

    graph_name: str

    pep_paths: list[GraphPath] = field(
        default_factory=list
    )

    sanction_paths: list[GraphPath] = field(
        default_factory=list
    )

    ownership_paths: list[GraphPath] = field(
        default_factory=list
    )

    shell_paths: list[GraphPath] = field(
        default_factory=list
    )

    execution_time_seconds: float = 0.0

    successful: bool = False

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    @property
    def total_paths(self) -> int:
        return (
            len(self.pep_paths)
            + len(self.sanction_paths)
            + len(self.ownership_paths)
            + len(self.shell_paths)
        )

    def to_dict(self) -> dict:

        return {

            "graph_name": self.graph_name,

            "pep_paths": len(
                self.pep_paths
            ),

            "sanction_paths": len(
                self.sanction_paths
            ),

            "ownership_paths": len(
                self.ownership_paths
            ),

            "shell_paths": len(
                self.shell_paths
            ),

            "total_paths": self.total_paths,

            "execution_time_seconds":
                self.execution_time_seconds,

            "successful":
                self.successful,

            "warnings":
                self.warnings,

            "errors":
                self.errors,
        }