"""
==========================================================
AML Investigation Platform

AML Detection Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.aml_detection.aml_finding import AMLFinding


@dataclass(slots=True)
class AMLDetectionResult:

    findings: list[AMLFinding] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    execution_time_seconds: float = 0.0

    successful: bool = False

    @property
    def total_findings(self) -> int:

        return len(self.findings)

    @property
    def high_risk_findings(self) -> int:

        return sum(

            1

            for finding in self.findings

            if finding.severity.value in {

                "HIGH",

                "CRITICAL",

            }

        )