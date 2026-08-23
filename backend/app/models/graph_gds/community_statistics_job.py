"""
==========================================================
AML Investigation Platform

Community Statistics Job

==========================================================
"""

from app.models.graph_gds.community_repository import (
    CommunityRepository,
)


class CommunityStatisticsJob:

    def __init__(
        self,
        repository: CommunityRepository,
    ):

        self._repository = repository

    def execute(self):

        return self._repository.calculate_community_statistics()