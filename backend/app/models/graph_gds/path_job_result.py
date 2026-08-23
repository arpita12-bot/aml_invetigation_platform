"""
==========================================================
AML Investigation Platform

Path Analytics Result
==========================================================
"""

from dataclasses import dataclass, field

from app.models.graph_gds.pep_path_result import PepPathResult
from app.models.graph_gds.sanction_path_result import SanctionPathResult
from app.models.graph_gds.ownership_path_result import OwnershipPathResult
from app.models.graph_gds.shell_path_result import ShellPathResult


@dataclass(slots=True)
class PathJobResult:

    graph_name: str

    pep_paths: list[PepPathResult] = field(default_factory=list)

    sanction_paths: list[SanctionPathResult] = field(default_factory=list)

    ownership_paths: list[OwnershipPathResult] = field(default_factory=list)

    shell_paths: list[ShellPathResult] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    execution_time_seconds: float = 0.0

    successful: bool = False

    def to_dict(self):

        return {

            "graph_name": self.graph_name,

            "pep_paths": [p.__dict__ for p in self.pep_paths],

            "sanction_paths": [p.__dict__ for p in self.sanction_paths],

            "ownership_paths": [p.__dict__ for p in self.ownership_paths],

            "shell_paths": [p.__dict__ for p in self.shell_paths],

            "warnings": self.warnings,

            "errors": self.errors,

            "execution_time_seconds": self.execution_time_seconds,

            "successful": self.successful,
        }