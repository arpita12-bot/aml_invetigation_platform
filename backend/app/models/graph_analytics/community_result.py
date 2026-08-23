"""
==========================================================
AML Investigation Platform

Community Result

Represents the community detected for an entity.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommunityResult:

    community_id: str

    community_size: int

    modularity: float

    suspicious_entities: int

    risk_score: float

    def to_dict(self) -> dict:

        return {

            "community_id": self.community_id,

            "community_size": self.community_size,

            "modularity": self.modularity,

            "suspicious_entities": self.suspicious_entities,

            "risk_score": self.risk_score,
        }