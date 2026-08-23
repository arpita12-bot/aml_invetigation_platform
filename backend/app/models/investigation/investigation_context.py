"""
==========================================================
AML Investigation Platform

Investigation Context

Responsibilities
----------------
✓ Carry investigation request
✓ Carry investigation graph
✓ Carry path analytics
✓ Carry shell intelligence
✓ Aggregate warnings
✓ Aggregate errors

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.models.graph_gds.path_job_result import (
    PathJobResult,
)

from app.models.investigation.investigation_graph import (
    InvestigationGraph,
)

from app.models.shell_pattern_result import (
    ShellPatternResult,
)

from app.models.graph_gds.centrality_metrics import (
    CentralityMetrics,
)

if TYPE_CHECKING:
    from app.models.investigation.investigation_request import (
        InvestigationRequest,
    )

from app.models.investigation.investigation_intelligence_result import (
    InvestigationIntelligenceResult,
)

@dataclass(slots=True)
class InvestigationContext:
    """
    Shared context passed throughout
    the complete AML investigation pipeline.
    """

    # -----------------------------------------------------
    # Investigation Request
    # -----------------------------------------------------

    request: "InvestigationRequest"

    # -----------------------------------------------------
    # Investigation Graph
    # -----------------------------------------------------

    investigation_graph: InvestigationGraph | None = None

    # -----------------------------------------------------
    # Graph Analytics
    # -----------------------------------------------------

    path_result: PathJobResult | None = None
    
    # -----------------------------------------------------
    # Graph Centrality Metrics
    # -----------------------------------------------------

    centrality_metrics: list[CentralityMetrics] = field(
        default_factory=list
    )
    
    
    intelligence: InvestigationIntelligenceResult | None = None

    # -----------------------------------------------------
    # Shell Intelligence
    # -----------------------------------------------------

    shell_result: ShellPatternResult | None = None

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)