"""
==========================================================
AML Investigation Platform

Base Graph Analyzer

Responsibilities
----------------
✓ Common interface for all graph analyzers
✓ Return RiskFactor objects
✓ Dataset agnostic

==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor


class BaseAnalyzer(ABC):
    """
    Base class for every graph analyzer.
    """

    @classmethod
    @abstractmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:
        """
        Analyze the graph and return risk factors.
        """
        raise NotImplementedError