"""
==========================================================
AML Investigation Platform

Triple Export Result

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class TripleExportResult:

    output_file: str

    total_triples: int = 0

    duplicate_triples: int = 0

    invalid_triples: int = 0

    exported_triples: int = 0

    execution_time_seconds: float = 0.0

    started_at: datetime | None = None

    finished_at: datetime | None = None

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    @property
    def success(self) -> bool:

        return len(self.errors) == 0