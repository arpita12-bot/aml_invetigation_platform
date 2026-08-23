"""
==========================================================
AML Investigation Platform

Path Analytics Execution Plan

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class PathExecutionPlan:

    max_depth: int = 6

    compute_shortest_paths: bool = True

    compute_pep_paths: bool = True

    compute_sanction_paths: bool = True

    compute_ownership_paths: bool = True