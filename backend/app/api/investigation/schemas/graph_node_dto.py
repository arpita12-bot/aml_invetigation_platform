"""
==========================================================
AML Investigation Platform

Graph Node DTO
==========================================================
"""

from pydantic import BaseModel, Field


class GraphNodeDTO(BaseModel):
    node_id: str = Field(..., description="Unique node identifier")

    label: str = Field(..., description="Neo4j node label")

    properties: dict = Field(
        default_factory=dict,
        description="Node properties",
    )