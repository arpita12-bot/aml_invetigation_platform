"""
==========================================================
AML Investigation Platform

Prediction Request

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PredictionRequest:

    head: str | None = None

    relation: str = ""

    tail: str | None = None

    top_k: int = 10

    threshold: float = 0.50