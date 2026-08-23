"""
==========================================================
AML Investigation Platform

Investigation Request DTO
==========================================================
"""

from pydantic import BaseModel, Field


class InvestigationRequestDTO(BaseModel):

    case_id: str

    analyst: str

    entity_id: str

    entity_type: str

    max_depth: int = Field(
        default=4,
        ge=1,
        le=10,
    )

    include_pep: bool = True

    include_sanctions: bool = True

    include_transactions: bool = True