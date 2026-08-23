"""
==========================================================
AML Investigation Platform

Shell Candidate Mapper

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.shell_candidate_dto import (
    ShellCandidateDTO,
)

from app.models.shell_candidate import (
    ShellCandidate,
)


class ShellCandidateMapper:
    """
    Converts shell candidates into API DTOs.
    """

    @staticmethod
    def map_candidates(

        candidates: list[ShellCandidate],

    ) -> list[ShellCandidateDTO]:

        return [

            ShellCandidateDTO(

                company_id=
                    candidate.company_id,

                company_name=
                    candidate.company_name,

                suspicion_score=
                    candidate.suspicion_score,

                risk_level=
                    candidate.risk_level,

                explanation=
                    candidate.explanation,

            )

            for candidate in candidates

        ]