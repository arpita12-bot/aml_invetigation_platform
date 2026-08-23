"""
==========================================================
AML Investigation Platform

Risk Score

Represents the calculated AML risk score.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiskScore:
    """
    AML Risk Score.
    """

    total_score: float

    prediction_score: float

    graph_score: float

    customer_score: float

    company_score: float

    transaction_score: float

    risk_level: str

    confidence: float

    def to_dict(self) -> dict:

        return {
            "total_score": self.total_score,
            "prediction_score": self.prediction_score,
            "graph_score": self.graph_score,
            "customer_score": self.customer_score,
            "company_score": self.company_score,
            "transaction_score": self.transaction_score,
            "risk_level": self.risk_level,
            "confidence": self.confidence,
        }