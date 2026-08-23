"""
==========================================================
AML Investigation Platform

Path Result DTO
==========================================================
"""

from pydantic import BaseModel, Field


class PathResultDTO(BaseModel):

    pep_path_count: int = 0

    sanction_path_count: int = 0

    ownership_path_count: int = 0

    shell_path_count: int = 0