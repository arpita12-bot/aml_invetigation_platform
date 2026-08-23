from dataclasses import dataclass, field

from app.models.risk.risk_factor import RiskFactor
from app.models.risk.risk_score import RiskScore


@dataclass(slots=True)
class RiskScoringResult:

    risk_score: RiskScore

    factors: list[RiskFactor] = field(default_factory=list)

    execution_time_seconds: float = 0.0

    successful: bool = True