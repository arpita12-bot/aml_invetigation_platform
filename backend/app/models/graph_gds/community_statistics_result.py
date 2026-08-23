"""
==========================================================
AML Investigation Platform

Community Statistics Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CommunityStatisticsResult:

    communities_processed: int

    nodes_updated: int

    execution_time_seconds: float

    successful: bool

    def to_dict(self):

        return {

            "communities_processed":
                self.communities_processed,

            "nodes_updated":
                self.nodes_updated,

            "execution_time_seconds":
                self.execution_time_seconds,

            "successful":
                self.successful,
        }