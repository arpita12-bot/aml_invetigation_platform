"""
==========================================================
AML Investigation Platform

AML Finding

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.aml_detection.aml_severity import AMLSeverity


@dataclass(slots=True)
class AMLFinding:
    """
    Represents one AML rule finding.
    """

    rule_name: str

    severity: AMLSeverity

    entity_id: str

    entity_type: str

    score: float

    description: str

    evidence: dict = field(default_factory=dict)