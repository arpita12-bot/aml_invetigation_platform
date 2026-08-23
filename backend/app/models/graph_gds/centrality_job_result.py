"""
==========================================================
AML Investigation Platform

Centrality Job Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CentralityJobResult:

    graph_name: str

    degree_written: int

    betweenness_written: int

    closeness_written: int

    pagerank_written: int

    execution_time_seconds: float

    successful: bool

    def to_dict(self):

        return {

            "graph_name": self.graph_name,

            "degree_written": self.degree_written,

            "betweenness_written": self.betweenness_written,

            "closeness_written": self.closeness_written,

            "pagerank_written": self.pagerank_written,

            "execution_time_seconds":
                self.execution_time_seconds,

            "successful":
                self.successful,
        }