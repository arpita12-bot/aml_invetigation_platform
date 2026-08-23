"""
==========================================================
AML Investigation Platform

Centrality Execution Plan

Controls which GDS algorithms should execute.

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CentralityExecutionPlan:

    run_degree: bool = True

    run_betweenness: bool = True

    run_closeness: bool = True

    run_pagerank: bool = True