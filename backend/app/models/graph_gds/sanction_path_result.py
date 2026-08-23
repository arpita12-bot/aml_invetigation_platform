"""
==========================================================
AML Investigation Platform

Sanction Path Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SanctionPathResult:

    source_entity_id: str

    sanction_id: str

    sanction_name: str

    sanction_program: str

    jurisdiction: str

    hop_count: int

    relationship_chain: list[str]

    node_chain: list[str]

    exposure_level: str

    path_risk_score: float