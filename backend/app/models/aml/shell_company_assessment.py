"""
==========================================================
AML Investigation Platform

Shell Company Assessment

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ShellCompanyAssessment:

    shell_score: float

    shared_directors: int

    shared_addresses: int

    shared_phone_numbers: int

    shared_devices: int

    circular_transactions: int

    recent_registration: bool

    recommendation: str

    def to_dict(self) -> dict:

        return {
            "shell_score": self.shell_score,
            "shared_directors": self.shared_directors,
            "shared_addresses": self.shared_addresses,
            "shared_phone_numbers": self.shared_phone_numbers,
            "shared_devices": self.shared_devices,
            "circular_transactions": self.circular_transactions,
            "recent_registration": self.recent_registration,
            "recommendation": self.recommendation,
        }