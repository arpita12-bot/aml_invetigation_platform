"""
==========================================================
AML Investigation Platform

Community Execution Plan

Responsibilities
----------------
✓ Configure community detection algorithms
✓ Enable selective execution of GDS analytics
✓ Reduce unnecessary computation

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommunityExecutionPlan:
    """
    Controls which community detection
    algorithms are executed.

    Similar to PathExecutionPlan and
    CentralityExecutionPlan.
    """

    # -----------------------------------------------------
    # Graph Algorithms
    # -----------------------------------------------------

    run_louvain: bool = True

    run_wcc: bool = True