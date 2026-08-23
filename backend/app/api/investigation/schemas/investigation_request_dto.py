"""
==========================================================
AML Investigation Platform

Investigation Request DTO

==========================================================
"""

from pydantic import BaseModel, Field


class InvestigationRequestDTO(BaseModel):
    """
    API request used to initiate an AML investigation.
    """

    entity_id: str = Field(
        ...,
        description="Root entity identifier.",
        examples=["CUST-100001"],
    )

    entity_type: str = Field(
        ...,
        description="Entity type.",
        examples=["CUSTOMER"],
    )

    analyst: str = Field(
        ...,
        description="Analyst executing the investigation.",
        examples=["john.doe"],
    )

    case_id: str = Field(
        ...,
        description="Investigation case identifier.",
        examples=["CASE-2026-0001"],
    )

    max_depth: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum graph traversal depth.",
    )

    include_transactions: bool = True

    include_pep: bool = True

    include_sanctions: bool = True

    include_devices: bool = False

    include_adverse_news: bool = True