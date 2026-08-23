"""
==========================================================
AML Investigation Platform

Community Detection Job Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommunityJobResult:

    graph_name: str

    communities_found: int

    modularity: float

    node_properties_written: int

    execution_time_seconds: float

    successful: bool

    def to_dict(self):

        return {

            "graph_name": self.graph_name,

            "communities_found": self.communities_found,

            "modularity": self.modularity,

            "node_properties_written":
                self.node_properties_written,

            "execution_time_seconds":
                self.execution_time_seconds,

            "successful":
                self.successful,
        }