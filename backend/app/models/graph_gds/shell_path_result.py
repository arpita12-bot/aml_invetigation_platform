"""
==========================================================
AML Investigation Platform

Shell Company Path Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ShellPathResult:

    source_entity_id: str

    shell_company_id: str

    shell_company_name: str

    hop_count: int

    ownership_chain: list[str]

    relationship_chain: list[str]

    community_id: int | None

    similarity_score: float

    page_rank: float

    link_prediction_score: float

    suspicion_score: float

    explanation: str