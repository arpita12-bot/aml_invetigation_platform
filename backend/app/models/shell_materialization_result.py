"""
==========================================================
AML Investigation Platform

Shell Materialization Result

Responsibilities
----------------
✓ Carry investigation graph
✓ Carry shell pattern result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.investigation.investigation_graph import (
    InvestigationGraph,
)

from app.models.shell_pattern_result import (
    ShellPatternResult,
)


@dataclass(slots=True)
class ShellMaterializationResult:
    """
    Result returned by the shell materialization pipeline.
    """

    investigation_graph: InvestigationGraph

    shell_result: ShellPatternResult