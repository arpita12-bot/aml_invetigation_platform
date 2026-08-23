"""
==========================================================
AML Investigation Platform

Investigation Recommendation

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class InvestigationRecommendation:

    priority: str

    action: str

    explanation: str

    requires_edd: bool

    requires_sar: bool

    freeze_account: bool

    notify_compliance: bool

    def to_dict(self) -> dict:

        return {
            "priority": self.priority,
            "action": self.action,
            "explanation": self.explanation,
            "requires_edd": self.requires_edd,
            "requires_sar": self.requires_sar,
            "freeze_account": self.freeze_account,
            "notify_compliance": self.notify_compliance,
        }