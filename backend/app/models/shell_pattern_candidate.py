"""
==========================================================
AML Investigation Platform

Shell Pattern Candidate

==========================================================
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ShellPatternCandidate:

    company_id: str

    company_name: str

    community_id: int | None

    community_size: int

    degree_centrality: float

    betweenness_centrality: float

    closeness_centrality: float

    page_rank: float

    similarity_score: float

    prediction_score: float

    ownership_layers: int

    pep_connections: int

    sanction_connections: int

    suspicious_transactions: int

    country: str

    industry: str

    evidence: list[str] = field(default_factory=list)