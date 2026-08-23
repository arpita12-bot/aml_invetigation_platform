"""
==========================================================
AML Investigation Platform

PEP Path Result

==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class PepPathResult:

    source_entity_id: str

    pep_id: str

    pep_name: str

    hop_count: int

    relationship_chain: list[str]

    node_chain: list[str]

    exposure_level: str

    path_risk_score: float