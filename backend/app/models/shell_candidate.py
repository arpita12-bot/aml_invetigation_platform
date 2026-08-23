from dataclasses import dataclass, field


@dataclass(slots=True)
class ShellCandidate:

    company_id: str

    company_name: str

    suspicion_score: float

    community_score: float

    centrality_score: float

    similarity_score: float

    ownership_score: float

    prediction_score: float

    pep_score: float

    sanction_score: float

    explanation: str

    evidence: list[str] = field(default_factory=list)