"""
==========================================================
AML Investigation Platform

Risk Factor

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiskFactor:
    """
    Represents one contributing factor
    in the overall AML risk score.
    """

    name: str
    score: float
    weight: float
    description: str

    entity_label: str | None = None
    entity_identifier: str | None = None