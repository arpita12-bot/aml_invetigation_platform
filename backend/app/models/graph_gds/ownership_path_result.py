"""
==========================================================
AML Investigation Platform

Ownership Path Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class OwnershipPathResult:

    source_entity_id: str

    target_company_id: str

    target_company_name: str

    ownership_percentage: float

    hop_count: int

    relationship_chain: list[str]

    node_chain: list[str]

    ownership_type: str

    path_risk_score: float