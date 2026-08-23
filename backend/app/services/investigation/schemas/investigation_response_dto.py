"""
==========================================================
AML Investigation Platform

Investigation Response DTO
==========================================================
"""

from pydantic import BaseModel, Field

from app.api.investigation.schemas.graph_node_dto import (
    GraphNodeDTO,
)

from app.api.investigation.schemas.graph_relationship_dto import (
    GraphRelationshipDTO,
)

from app.api.investigation.schemas.shell_candidate_dto import (
    ShellCandidateDTO,
)

from app.api.investigation.schemas.path_result_dto import (
    PathResultDTO,
)


class InvestigationResponseDTO(BaseModel):

    case_id: str

    successful: bool

    execution_time_seconds: float

    graph_nodes: list[GraphNodeDTO] = Field(
        default_factory=list,
    )

    graph_relationships: list[
        GraphRelationshipDTO
    ] = Field(
        default_factory=list,
    )

    shell_candidates: list[
        ShellCandidateDTO
    ] = Field(
        default_factory=list,
    )

    path_summary: PathResultDTO

    warnings: list[str] = Field(
        default_factory=list,
    )

    errors: list[str] = Field(
        default_factory=list,
    )