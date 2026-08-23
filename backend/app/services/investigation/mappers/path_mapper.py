"""
==========================================================
AML Investigation Platform

Path Mapper

==========================================================
"""

from __future__ import annotations

from app.api.investigation.schemas.path_result_dto import (
    PathResultDTO,
)

from app.models.graph_gds.path_job_result import (
    PathJobResult,
)


class PathMapper:
    """
    Converts PathJobResult into DTO.
    """

    @staticmethod
    def map(

        result: PathJobResult,

    ) -> PathResultDTO:

        return PathResultDTO(

            pep_path_count=
                len(result.pep_paths),

            sanction_path_count=
                len(result.sanction_paths),

            ownership_path_count=
                len(result.ownership_paths),

            shell_path_count=
                len(result.shell_paths),

        )