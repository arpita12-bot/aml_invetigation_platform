"""
==========================================================
AML Investigation Platform

Investigation Result

Represents the complete AML investigation response
returned to the Investigator Dashboard.

Responsibilities
----------------
✓ Store investigation results
✓ Support multiple predicted relationships
✓ Store execution metadata
✓ Store warnings and errors

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.models.aml.investigation_item import (
    InvestigationItem,
)


@dataclass(slots=True)
class InvestigationResult:
    """
    Complete AML investigation result.

    One investigation may contain intelligence for
    multiple predicted relationships returned by
    the link prediction engine.
    """

    items: list[InvestigationItem] = field(default_factory=list)

    execution_time_seconds: float = 0.0

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        """
        Total number of investigated predictions.
        """
        return len(self.items)

    @property
    def has_warnings(self) -> bool:
        """
        Indicates whether warnings were generated.
        """
        return len(self.warnings) > 0

    @property
    def has_errors(self) -> bool:
        """
        Indicates whether errors occurred.
        """
        return len(self.errors) > 0

    @property
    def is_successful(self) -> bool:
        """
        Investigation completed successfully.
        """
        return not self.has_errors

    def to_dict(self) -> dict:
        """
        Convert investigation result to dictionary.
        """

        return {
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "total_items": self.total_items,
            "execution_time_seconds": self.execution_time_seconds,
            "warnings": self.warnings,
            "errors": self.errors,
            "is_successful": self.is_successful,
        }