"""
==========================================================
AML Investigation Platform

Centrality Execution Plan

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CentralityExecutionPlan:

    compute_pagerank: bool = True

    compute_degree: bool = True

    compute_betweenness: bool = True