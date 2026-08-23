"""
==========================================================
AML Investigation Platform

Graph Relationship DTO
==========================================================
"""

from pydantic import BaseModel, Field


class GraphRelationshipDTO(BaseModel):
    relationship_type: str = Field(
        ...,
        description="Relationship type",
    )

    source_id: str = Field(
        ...,
        description="Source node id",
    )

    target_id: str = Field(
        ...,
        description="Target node id",
    )

    properties: dict = Field(
        default_factory=dict,
        description="Relationship properties",
    )