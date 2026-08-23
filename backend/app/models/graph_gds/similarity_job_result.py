"""
==========================================================
AML Investigation Platform

Similarity Job Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SimilarityJobResult:

    graph_name: str

    relationships_written: int

    similarity_pairs: int

    execution_time_seconds: float

    successful: bool

    def to_dict(self):

        return {

            "graph_name": self.graph_name,

            "relationships_written":
                self.relationships_written,

            "similarity_pairs":
                self.similarity_pairs,

            "execution_time_seconds":
                self.execution_time_seconds,

            "successful":
                self.successful,
        }